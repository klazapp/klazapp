# 04 / Layout as data, not component logic

**Project:** [Bento Grid Builder](https://github.com/klazapp/bento-grid-builder)

## The constraint

A dashboard card can keep doing the same job while its position, span or surrounding layout changes. Mixing that placement logic into the component makes simple rearrangements touch behaviour they should not affect.

## What the library separates

Card definitions identify the components. Layouts describe their placement. Data mappings select the props that each card receives from application data.

The public API supports preset layouts, explicit placements, breakpoint-specific arrangements and a fluent builder. For example, using the documented API:

```tsx
import { layoutBuilder } from "bento-grid-builder";

const layout = layoutBuilder(4)
  .gap(16)
  .place("hero", 1, 1, { colSpan: 2, rowSpan: 2 })
  .place("stats1", 3, 1)
  .place("stats2", 4, 1)
  .place("chart", 3, 2, { colSpan: 2 })
  .build();
```

This is an illustrative configuration, not a claim that the snippet was executed to capture an application screenshot. The profile's layout diagram is based on the four-column custom-layout example in the repository README.

## The boundary

Changing a card's placement need not change its rendering behaviour or data mapping. Likewise, changing a data selector need not force a new layout definition.

## The trade-off

A declarative layer is useful when arrangements repeat or vary. It also adds vocabulary that the next engineer must learn. For a single fixed page, ordinary CSS grid may be clearer and cheaper to maintain.

The abstraction is about separating axes of change, not avoiding CSS or promising that every new design can be expressed without extending the library.

## Inspect it

[Custom layouts](https://github.com/klazapp/bento-grid-builder#custom-layouts) · [Responsive layouts](https://github.com/klazapp/bento-grid-builder#responsive-layouts) · [Published preview](https://github.com/klazapp/bento-grid-builder/blob/main/assets/bento-preview.png)

[Back to the profile](../README.md#ui)
