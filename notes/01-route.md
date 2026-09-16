# 01 / The bridge disappears mid-route

**Project:** [Grid-Based Pathfinding](https://github.com/klazapp/UNITY-GridBased-Pathfinding)

## The constraint

The player may already be moving when world connectivity changes. Keeping a list of waypoints is not enough: the system also has to remember the destination and respond when a route becomes unavailable or possible again.

## What the implementation does

`NavigationWorldAdapter` maps scene locations into a plain-C# graph. The navigation assembly forbids Unity engine references with `noEngineReferences: true`. The route finder queries `IRouteQuery`; positions and transforms remain outside the search.

Graph mutations update `TopologyVersion` and emit `TopologyChanged`. Route results carry the version they were calculated against. The controller subscribes to topology changes and requests a new route whenever a destination is pending.

```csharp
// PlayerController.cs — implementation excerpt
private void TopologyChangedCallback()
{
    if (destinationNode == null)
        return;

    RequestRoute();
}
```

On a failed search, movement stops but `destinationNode` remains set. A later change can therefore resume the intended journey without another click. Successful arrival clears the destination.

## The deliberate boundary

The graph describes connectivity; it does not know how Unity draws tiles or receives clicks. This makes the navigation layer testable without scene objects. The repository includes edit-mode tests for graph changes, unavailable locations, route results and deterministic behaviour.

## The trade-off

The controller currently replans after every topology event while a destination is pending. It does not gate that request on an explicit version-equality check. Route version metadata and the controller's event-driven replanning are related mechanisms, not the same operation.

This is simple for the demo. With many agents or many changes per frame, a useful next question is whether to batch mutations, coalesce events, or check the remaining route before recalculating. Those are extension ideas, not capabilities claimed for the present controller.

## Inspect it

[Controller](https://github.com/klazapp/UNITY-GridBased-Pathfinding/blob/main/Assets/Scripts/Player/PlayerController.cs) · [Graph and route types](https://github.com/klazapp/UNITY-GridBased-Pathfinding/tree/main/Assets/Scripts/Navigation) · [Tests](https://github.com/klazapp/UNITY-GridBased-Pathfinding/tree/main/Assets/Tests/EditMode)

The README describes a bridge-toggle demo. The linked original GIF is a routing showcase; it is not presented here as a new recording of bridge invalidation.

[Back to the profile](../README.md#runtime)
