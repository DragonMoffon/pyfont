# PYFONT

 <!-- Th PRs welcome button links GitHub doc b/c the original makeapullrequest.com's gone. -->
 [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) [![Tests (main)](https://github.com/DragonMoffon/pyfont/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/DragonMoffon/pyfont/actions/workflows/test.yaml?branch=main)

A zero-dependency Python-only library for reading TTF and OTF fonts.

> [!IMPORTANT]
> This project only supports reading fonts!
> To write font data, you will need a different libary.

Support for [woff][] and woff2 is a possibility in the future.

[woff]: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fonts/WOFF


## Features

The basic Font, and Collection objects:

- do no work to process the fonts
- partly implement v1.9.1 of [The Microsoft OpenType Specification][]


### Goals

Table definitions and parsing aim to implement the
following documents:

1. [The Microsoft OpenType Specification][]
2. [The Apple TrueType Reference Manual][]

In the event of a conflict, the OpenType (OTF) specification
takes precedence. Lists of planned and finished OTF tables
tables are located in the [TABLE PROGRESS](#table-progress)
section below.

[The Microsoft OpenType Specification]: https://learn.microsoft.com/en-us/typography/opentype/spec/otf
[The Apple TrueType Reference Manual]: https://developer.apple.com/fonts/TrueType-Reference-Manual/


## Contributing

## First-Time Setup

Make sure you have Python 3.13 or higher installed, then:
1. Fork and clone the repo
2. Create and activate a virtual environment
3. `pip install --upgrade setuptools`
4. `pip install -I -e .[dev]`
5. If install succeeds, run `python -m pytest`

Tests should pass. If something goes wrong, please [file an issue][].


## Project Structure

### Test Fonts

The test fonts in the [`fonts/`](fonts/) folder should be
attributed in accordance with their licenses. They:

- are intended for testing only
- will **never** be included in any PyPI releases

If a font is improperly licensed, please either [file an issue][]
or [open a pull request][].

Does not yet validate checksums or do any sort of file sanitiation. 

[file an issue]: https://github.com/DragonMoffon/pyfont/issues/new
[open a pull request]: https://github.com/DragonMoffon/pyfont/pulls/compare

### TABLE PROGRESS

#### Complete

##### Collection Tables
- [x] TTC Header
- [x] Table Directory

##### TTF Tables
- [ ] acnt (accent attachment)
- [ ] ankr (anchor point)
- [x] avar (axis variation)
- [ ] bdat (bitmap data)
- [ ] bhed (bitmap font header)
- [ ] bloc (bitmap location)
- [ ] bsln (baseline)
- [ ] cmap (character code mapping)
- [ ] cvar (CVT variation)
- [x] cvt (control value)
- [ ] EBSC (embedded bitmap scaling control)
- [ ] fdsc (font descriptor)
- [ ] feat (layout feature)
- [ ] fmtx (font metrics)
- [ ] fond (font family compatibility)
- [x] fpgm (font program)
- [x] fvar (font variation)
- [ ] gasp (grid-fitting and scan-conversion procedure)
- [ ] glyf (glyph outline)
- [ ] gvar (glyph variation)
- [ ] hdmx (horizontal device metrics)
- [x] head (font header)
- [x] hhea (horizontal header)
- [x] hmtx (horizontal metrics)
- [ ] just (justification)
- [ ] kern (kerning)
- [ ] kerx (extended kerning)
- [ ] lcar (ligature caret)
- [ ] loca (glyph location)
- [ ] ltag (language tag)
- [x] maxp (maximum profile)
- [ ] meta (metadata)
- [ ] mort (metamorphosis) table (deprecated)
- [ ] morx (extended metamorphosis)
- [ ] name (name)
- [ ] opbd (optical bounds)
- [x] OS/2 (compatibility)
- [x] post (glyph name and PostScript compatibility)
- [ ] prep (control value program)
- [ ] prop (properties)
- [ ] sbix (extended bitmaps)
- [ ] trak (tracking)
- [ ] vhea (vertical header)
- [ ] vmtx (vertical metrics)
- [ ] xref (cross-reference)
- [ ] Zapf (glyph reference)

##### OTF Tables
- [ ] BASE (baseline)
- [ ] CBDT (color bitmap data)
- [ ] CBLC (color bitmap location)
- [ ] CFF (compact font format)
- [ ] CFF2 (compact font format v2)
- [ ] COLR (color)
- [ ] CPAL (color palette)
- [ ] DSIG (digital signature)
- [ ] EBDT (embedded bitmap data)
- [ ] EBLC (embadded bitmap location)
- [ ] GDEF (glyph definition)
- [ ] GPOS (glyph positioning)
- [ ] GSUB (glyph substitution)
- [ ] HVAR (horizontal metrix variation)
- [ ] JSTF (justification)
- [ ] LTSH (linear threshold)
- [ ] MATH (mathematical typesetting)
- [ ] MERG (merge)
- [ ] MVAR (metrics variation)
- [x] PCLT (PCL 5)
- [ ] STAT (style attributes)
- [ ] SVG (scalar vector graphics)
- [ ] VDMX (vertical device metrics)
- [ ] VORG (vetical origin)
- [ ] VVAR (vertical metrics variations)

#### Definition
- [ ] acnt
- [x] ankr
- [x] avar
- [ ] BASE
- [ ] bdat
- [ ] bhed
- [ ] bloc
- [ ] bsln
- [ ] CBDT
- [ ] CBLC
- [ ] CFF
- [ ] CFF2
- [x] cmap
- [ ] COLR
- [ ] CPAL
- [ ] cvar
- [x] cvt 
- [x] DSIG
- [ ] EBDT
- [ ] EBLC
- [ ] EBSC
- [ ] fdsc
- [ ] feat
- [ ] fmtx
- [ ] fond
- [x] fpgm
- [x] fvar
- [x] gasp
- [ ] GDEF
- [x] glyf
- [ ] GPOS
- [ ] GSUB
- [ ] gvar
- [ ] hdmx
- [x] head
- [x] hhea
- [x] hmtx
- [ ] HVAR
- [ ] JSTF
- [ ] just
- [ ] kern
- [ ] kerx
- [ ] lcar
- [x] loca
- [ ] ltag
- [ ] LTSH
- [ ] MATH
- [x] maxp
- [ ] MERG
- [ ] meta
- [ ] mort
- [ ] morx
- [ ] MVAR
- [x] name
- [ ] opbd
- [x] OS/2
- [x] PCLT
- [x] post
- [x] prep
- [ ] prop
- [x] sbix
- [ ] STAT
- [x] SVG
- [ ] trak
- [ ] VDMX
- [ ] vhea
- [ ] vmtx
- [ ] VORG
- [ ] VVAR
- [ ] xref
- [ ] Zapf

#### Parsing
- [ ] acnt
- [ ] ankr
- [x] avar
- [ ] BASE
- [ ] bdat
- [ ] bhed
- [ ] bloc
- [ ] bsln
- [ ] CBDT
- [ ] CBLC
- [ ] CFF
- [ ] CFF2
- [x] cmap
- [ ] COLR
- [ ] CPAL
- [ ] cvar
- [x] cvt 
- [x] DSIG
- [ ] EBDT
- [ ] EBLC
- [ ] EBSC
- [ ] fdsc
- [ ] feat
- [ ] fmtx
- [ ] fond
- [x] fpgm
- [x] fvar
- [ ] gasp
- [ ] GDEF
- [ ] glyf
- [ ] GPOS
- [ ] GSUB
- [ ] gvar
- [ ] hdmx
- [x] head
- [x] hhea
- [x] hmtx
- [ ] HVAR
- [ ] JSTF
- [ ] just
- [ ] kern
- [ ] kerx
- [ ] lcar
- [ ] loca
- [ ] ltag
- [ ] LTSH
- [ ] MATH
- [x] maxp
- [ ] MERG
- [ ] meta
- [ ] mort
- [ ] morx
- [ ] MVAR
- [x] name **possibly missing some encodings*
- [ ] opbd
- [x] OS/2
- [x] PCLT
- [x] post
- [ ] prep
- [ ] prop
- [ ] sbix
- [ ] STAT
- [ ] SVG
- [ ] trak
- [ ] VDMX
- [ ] vhea
- [ ] vmtx
- [ ] VORG
- [ ] VVAR
- [ ] xref
- [ ] Zapf
