# HANMA — Estudio web

La página que presenta los tres sitios de muestra a un cliente. Español, inglés
y árabe con RTL real, en un solo `index.html`.

**Verlo en local** (Chrome bloquea `file://` para esto):

```bash
cd ~/projects/estudio-web && python3 -m http.server 8098
```

<http://localhost:8098/>

## Para qué existe

Los tres sitios —NAHAR, BUNN y ATLAS— llevaban publicados desde principios de
septiembre sin nada que los enmarcara. Enviar tres enlaces sueltos obliga al
cliente a deducir por su cuenta qué demuestran. Esta página lo dice: qué hay
en cada uno, cómo se trabaja, qué cuesta y qué **no** se hace.

## Las nueve páginas

`Inicio` · `Trabajos` · `Método` · `Precio` · `Cómo está hecho` · `Contacto` ·
`Legal` · `Mapa del sitio` · `404`

Las seis primeras son páginas largas con su índice; las tres últimas son de
servicio. Ninguna baja de 500 palabras en español, que es el listón por debajo
del cual una página no está terminada.

## Lo que no es relleno

- **Configurador de alcance** (`#/precios`). Idiomas, número de páginas largas
  y piezas a medida salen con precio, semanas, mes de entrega y el calendario
  de pagos 40/30/30. La base no está inventada: son los **2.400 €** ya cerrados
  por escrito con un cliente real para un sitio trilingüe de seis páginas, y
  con la configuración por defecto el desglose sale 960 / 720 / 720.
- **Medidas reales** (`#/tecnica`). El peso de los tres sitios medido el
  8-9-2026 con `gzip -c index.html | wc -c`, con la orden escrita en la propia
  página para que cualquiera repita la medición.
- **Fichas de caso**. Apartados, rutas, claves y peso de cada sitio salen de la
  constante `CASOS`, no de un texto: cambiar una cifra la cambia en los tres
  idiomas a la vez.

## Antes de publicarlo

1. **`var CORREO = ""`** en la cabecera del script. Está vacío a propósito:
   prefiere un hueco visible a una dirección inventada. Mientras siga vacío, la
   página de contacto dice «pendiente de configurar» en los tres idiomas.
2. **`HANMA`** es el nombre comercial. Se cambia en el `<title>`, en el logotipo
   y en las claves `t*` de los tres diccionarios.

## Comprobado

```
142 claves × 3 idiomas    paridad ✔ · 0 sin traducir · formas paralelas ✔
9 rutas × 3 idiomas       0 fugas de idioma en las 27 combinaciones
desborde horizontal       0 px a 380 y a 1280, en LTR y en RTL
configurador              4 configuraciones: el desglose suma el total exacto
dígitos                   árabe-índicos en recuentos y fechas; latinos en precios
bidi                      importes aislados con dir="ltr" dentro del árabe
peso transferido          46 kB comprimido, el sitio entero
```

---

Las tres empresas de los ejemplos son ficticias. Las cifras de sus calculadoras
son de modelo; los cálculos, reales.
