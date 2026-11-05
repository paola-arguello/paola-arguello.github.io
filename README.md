# Lunaland

Source for my portfolio site, https://paola-arguello.github.io.

The site is about interpreting biological data: how results are built, where they break, and how to explain them. It has four parts. Projects are things I built. The Pitfalls Lab has short modules on common analysis mistakes. The Crosswalk has field notes. The Concept Atlas is a table of concepts that link the rest together.

AI assistants (including Claude by Anthropic) were used to help draft text and write and review code. I review every change before it is merged. See the About page for details.

## Build

The site is a Quarto website. R packages are managed with renv.

```r
renv::restore()
```

```bash
quarto render
```

Output goes to `docs/`. GitHub Pages serves the site from that folder, so commit the `docs/` changes together with the source changes.

## Layout

```
_quarto.yml        site config, navbar, footer
index.qmd          home
about.qmd
projects/          project pages
pitfalls/          Pitfalls Lab modules
crosswalk/         Crosswalk posts
atlas/             Concept Atlas (concepts.csv is the data)
assets/            images, figures, CV
scripts/           scripts that generate site figures
styles.css
docs/              rendered site (do not edit by hand)
```

`scripts/batch_effects_pca.py` makes the figure on the Batch Effects page. It needs Python with numpy and matplotlib. Run it from the repository root.
