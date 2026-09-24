#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fair_eval.py — Evaluación FAIR automatizada de los productos de datos de CITRIDATA.

Mide, sobre los artefactos reales de un paquete (schema.json, context.jsonld,
examples/, doc/, notes.yaml, ADOPTERS.yaml), 19 indicadores binarios agrupados en
las cuatro dimensiones FAIR, y produce la tabla 7 del artículo.

Uso:
    python3 fair_eval.py --despues <carpeta_modelos_publicados>
    python3 fair_eval.py --despues <pub> --antes <carpeta_originales>

La carpeta de "antes" debe contener, por cada conjunto, una subcarpeta con el
volcado tal y como salió del sistema de gestión del proveedor (el .csv/.xlsx y lo
que lo acompañara). Lo que no exista, no puntúa.

Salidas: fair_resultados.csv, fair_resultados.json, tabla7.md, indicadores.md
"""
import argparse, json, os, re, sys, csv, unicodedata

# --------------------------------------------------------------- indicadores
IND = {
 "F": [("F1", "Identificador global, único y resoluble ($id https)"),
       ("F2", "Metadatos descriptivos ricos (title + description sustantiva)"),
       ("F3", "El identificador consta dentro de los propios metadatos"),
       ("F4", "Etiquetas de descubrimiento mínimas (UCO, ATDFIWARE + temática)"),
       ("F5", "Cobertura declarada (temporal y/o geográfica)")],
 "A": [("A1", "Acceso por protocolo abierto y estandarizado (HTTPS)"),
       ("A2", "Ejemplo inspeccionable sin autenticación"),
       ("A3", "Metadatos accesibles con independencia del dato"),
       ("A4", "Condiciones de acceso y uso declaradas")],
 "I": [("I1", "Lenguaje formal de representación (JSON Schema válido)"),
       ("I2", "Vocabulario compartido publicado (context.jsonld)"),
       ("I3", "Reutiliza vocabularios comunes (GSMA / Location-Commons)"),
       ("I4", "≥90% de atributos anclados a schema.org"),
       ("I5", "Referencias cualificadas a otras entidades (Relationship NGSI-LD)")],
 "R": [("R1", "Licencia explícita"),
       ("R2", "Procedencia declarada (derivedFrom / notes / ADOPTERS)"),
       ("R3", "Documentación de uso no trivial"),
       ("R4", "≥90% de atributos con descripción redactada en inglés"),
       ("R5", "Conforme al estándar de comunidad (estructura SDM completa)")],
}
DIMS = ["F", "A", "I", "R"]

SDM_FILES = ["schema.json", "context.jsonld", "notes.yaml", "ADOPTERS.yaml",
             os.path.join("doc", "README.md"),
             os.path.join("examples", "example-keyvalues.json")]

ES_STOP = {"de", "la", "el", "los", "las", "del", "para", "por", "con", "una",
           "que", "y", "en", "al", "se", "su", "sus", "año", "datos"}


def read_json(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def properties_of(schema):
    """Todas las propiedades declaradas, incluidas las de los bloques allOf."""
    props = {}
    if not isinstance(schema, dict):
        return props
    props.update(schema.get("properties", {}) or {})
    for blk in schema.get("allOf", []) or []:
        if isinstance(blk, dict):
            props.update(blk.get("properties", {}) or {})
    return {k: v for k, v in props.items() if isinstance(v, dict)}


def looks_english(text):
    """Heurística: quita el prefijo normalizado y busca palabras vacías españolas."""
    t = re.sub(r"^(Property|Relationship|GeoProperty)\.", "", text or "")
    t = re.sub(r"Model:\s*'[^']*'\.?", "", t)
    t = re.sub(r"Units:\s*'[^']*'\.?", "", t)
    t = unicodedata.normalize("NFKD", t.lower())
    words = re.findall(r"[a-záéíóúñ]+", t)
    if len(words) < 2:
        return False
    hits = sum(1 for w in words if w in ES_STOP)
    return hits / len(words) < 0.18


def evaluate(folder, name):
    """Devuelve {indicador: 0|1} midiendo los ficheros que existan en folder."""
    r = {k: 0 for dim in DIMS for k, _ in IND[dim]}
    ev = {}
    sp = os.path.join(folder, "schema.json")
    schema = read_json(sp) if os.path.exists(sp) else None
    props = properties_of(schema) if schema else {}
    data_props = {k: v for k, v in props.items() if k not in ("id", "type")}

    # ---- F
    if schema:
        sid = str(schema.get("$id", ""))
        r["F1"] = int(sid.startswith("https://"))
        desc = str(schema.get("description", ""))
        r["F2"] = int(bool(schema.get("title")) and len(desc) >= 40)
        r["F3"] = int(bool(sid))
        tags = [str(t).upper() for t in (schema.get("modelTags") or [])]
        r["F4"] = int("UCO" in tags and "ATDFIWARE" in tags and len(tags) >= 3)
        cover = bool(re.search(r"\b(19|20)\d{2}\b", desc)) or \
                bool(re.search(r"(andalus|andaluc|spain|españa|provinc|region|polygon|parcel)", desc, re.I))
        geo = any("Location-Commons" in str(b.get("$ref", "")) for b in (schema.get("allOf") or []) if isinstance(b, dict))
        r["F5"] = int(cover or geo)
        ev["cobertura"] = {"texto": cover, "geo": geo}
    # ---- A
    r["A1"] = int(bool(schema) and str(schema.get("$id", "")).startswith("https://"))
    r["A2"] = int(os.path.exists(os.path.join(folder, "examples", "example-keyvalues.json")))
    r["A3"] = int(os.path.exists(sp))
    r["A4"] = int(bool(schema and schema.get("license")))
    # ---- I
    r["I1"] = int(bool(schema) and bool(schema.get("$schema")) and bool(props))
    r["I2"] = int(os.path.exists(os.path.join(folder, "context.jsonld")))
    refs = " ".join(str(b.get("$ref", "")) for b in (schema.get("allOf") or []) if isinstance(b, dict)) if schema else ""
    r["I3"] = int("GSMA-Commons" in refs)
    anchored = [k for k, v in data_props.items() if "schema.org" in str(v.get("description", ""))]
    pct_anchor = len(anchored) / len(data_props) if data_props else 0
    r["I4"] = int(pct_anchor >= 0.90)
    r["I5"] = int(any(str(v.get("description", "")).strip().startswith("Relationship")
                      for v in data_props.values()))
    # ---- R
    r["R1"] = r["A4"]
    prov = bool(schema and schema.get("derivedFrom")) or \
        os.path.exists(os.path.join(folder, "notes.yaml")) or \
        os.path.exists(os.path.join(folder, "ADOPTERS.yaml"))
    r["R2"] = int(prov)
    dp = os.path.join(folder, "doc", "README.md")
    r["R3"] = int(os.path.exists(dp) and os.path.getsize(dp) > 400)
    eng = [k for k, v in data_props.items() if looks_english(str(v.get("description", "")))]
    pct_eng = len(eng) / len(data_props) if data_props else 0
    r["R4"] = int(pct_eng >= 0.90)
    r["R5"] = int(all(os.path.exists(os.path.join(folder, f)) for f in SDM_FILES))

    ev.update({
        "n_atributos": len(data_props),
        "pct_schema_org": round(pct_anchor * 100, 1),
        "pct_ingles": round(pct_eng * 100, 1),
        "no_ancladas": sorted(set(data_props) - set(anchored)),
        "no_inglesas": sorted(set(data_props) - set(eng)),
        "faltan_ficheros": [f for f in SDM_FILES if not os.path.exists(os.path.join(folder, f))],
    })
    return r, ev


def score(r):
    return {d: sum(r[k] for k, _ in IND[d]) for d in DIMS}


def maxima():
    return {d: len(IND[d]) for d in DIMS}


def scan(root):
    out = {}
    if not root or not os.path.isdir(root):
        return out
    for n in sorted(os.listdir(root)):
        p = os.path.join(root, n)
        if os.path.isdir(p) and not n.startswith("."):
            out[n] = p
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--despues", required=True)
    ap.add_argument("--antes", default=None)
    ap.add_argument("--out", default=".")
    a = ap.parse_args()

    pub, raw = scan(a.despues), scan(a.antes)
    if not pub:
        sys.exit("No se han encontrado paquetes en --despues")
    MX = maxima()
    rows, detail = [], {}

    for name, folder in pub.items():
        rp, ev = evaluate(folder, name)
        sp_ = score(rp)
        if name in raw:
            rr, _ = evaluate(raw[name], name)
            sr = score(rr)
            has_before = True
        else:
            sr, has_before = {d: None for d in DIMS}, False
        rows.append({"conjunto": name, "antes": sr, "despues": sp_, "tiene_antes": has_before})
        detail[name] = {"indicadores": rp, "evidencia": ev}

    # ---------- CSV
    with open(os.path.join(a.out, "fair_resultados.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["conjunto"] + [f"{d}_{s}" for d in DIMS for s in ("antes", "despues")]
                   + ["global_despues_pct"])
        for r in rows:
            tot = sum(r["despues"][d] for d in DIMS)
            w.writerow([r["conjunto"]]
                       + [v for d in DIMS for v in (r["antes"][d] if r["antes"][d] is not None else "", r["despues"][d])]
                       + [round(100 * tot / sum(MX.values()), 1)])

    # ---------- JSON
    with open(os.path.join(a.out, "fair_resultados.json"), "w", encoding="utf-8") as f:
        json.dump({"maximos": MX, "filas": rows, "detalle": detail}, f, ensure_ascii=False, indent=2)

    # ---------- tabla 7 en markdown
    L = ["| Conjunto | F antes / después | A antes / después | I antes / después | R antes / después | Global |",
         "| --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        cells = []
        for d in DIMS:
            b = r["antes"][d]
            cells.append(f"{'—' if b is None else b} / {r['despues'][d]}  (máx. {MX[d]})")
        tot = sum(r["despues"][d] for d in DIMS)
        L.append(f"| `{r['conjunto']}` | " + " | ".join(cells) + f" | {round(100*tot/sum(MX.values()))} % |")
    n = len(rows)
    med = {d: sum(r["despues"][d] for r in rows) / n for d in DIMS}
    L.append("| **Media** | " + " | ".join(f"**{'—' if not any(r['tiene_antes'] for r in rows) else ''} / {med[d]:.1f}**" for d in DIMS)
             + f" | **{round(100*sum(med.values())/sum(MX.values()))} %** |")
    open(os.path.join(a.out, "tabla7.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    # ---------- catálogo de indicadores
    I = ["| Dim. | Id | Indicador |", "| --- | --- | --- |"]
    for d in DIMS:
        for k, t in IND[d]:
            I.append(f"| {d} | {k} | {t} |")
    open(os.path.join(a.out, "indicadores.md"), "w", encoding="utf-8").write("\n".join(I) + "\n")

    # ---------- resumen por consola
    print(f"Paquetes evaluados: {n}   (baseline 'antes': {'sí' if raw else 'no aportado'})")
    print("-" * 78)
    for r in rows:
        tot = sum(r["despues"][d] for d in DIMS)
        print(f"{r['conjunto']:<28} " + "  ".join(f"{d}{r['despues'][d]}/{MX[d]}" for d in DIMS)
              + f"   global {round(100*tot/sum(MX.values())):>3} %")
    print("-" * 78)
    print("Medias: " + "  ".join(f"{d} {med[d]:.2f}/{MX[d]}" for d in DIMS)
          + f"   global {round(100*sum(med.values())/sum(MX.values()))} %")
    print("\nIncidencias detectadas:")
    any_i = False
    for name, dd in detail.items():
        ev, ind = dd["evidencia"], dd["indicadores"]
        msgs = []
        if ev["faltan_ficheros"]:
            msgs.append("faltan " + ", ".join(ev["faltan_ficheros"]))
        if ev["pct_schema_org"] < 100:
            msgs.append(f"schema.org en {ev['pct_schema_org']}% de atributos")
        if ev["pct_ingles"] < 100:
            msgs.append(f"inglés en {ev['pct_ingles']}% de atributos")
        if msgs:
            any_i = True
            print(f"  · {name}: " + "; ".join(msgs))
    if not any_i:
        print("  (ninguna)")


if __name__ == "__main__":
    main()
