# 03 / How much work can the renderer avoid?

**Project:** [DMICustomDrawCall — Jobified](https://github.com/klazapp/UNITY-DMICustomDrawCall-Jobified)

## The constraint

An instanced scene can still do unnecessary work. A useful optimization must account for visibility, transform updates, data preparation and draw submission—not just the number of objects in the scene.

## What is published

The project combines custom culling with `DrawMeshInstanced`, a jobified system for position/scale/rotation, and material property blocks for per-instance colour. Its README documents Burst compatibility and links a recorded demo.

The profile's graphic explains that mechanism. It is not a Unity screenshot, a hardware measurement, or a comparison against another renderer.

## The trade-off

Culling itself has a cost. A mostly visible scene can pay for checks that reject little; a largely hidden scene may avoid enough rendering work to justify them. Job scheduling, memory access, synchronization and data copying also affect the result.

Moving work off the main thread does not automatically reduce total work, and fewer draw submissions do not by themselves prove lower GPU frame time.

## What a useful comparison would measure

This is a proposed verification protocol, not a report of measurements already completed:

- Hold hardware, scene content, camera path, build configuration and rendering settings constant.
- Compare CPU frame time, worker activity and GPU frame time, rather than only average FPS.
- Include mostly-visible and mostly-culled views so the visibility-work trade-off is observable.
- Separate cold-start effects from steady-state behaviour.

The repository's TODO lists a jobified/non-jobified performance comparison. No improvement percentage or “5,000 objects at 60 FPS” result is attached to this repository in the profile.

## Inspect it

[Project documentation](https://github.com/klazapp/UNITY-DMICustomDrawCall-Jobified#description) · [Implementation](https://github.com/klazapp/UNITY-DMICustomDrawCall-Jobified/tree/main/Assets/Scripts) · [Recorded demo](https://github.com/klazapp/UNITY-DMICustomDrawCall-Jobified/blob/main/Assets/GifShowCase/Showcase-1-Bounce.gif)

This is an older Unity experiment. Its README's API comparisons should be read in that historical context, not as universal claims about current Unity rendering APIs.

[Back to the profile](../README.md#rendering)
