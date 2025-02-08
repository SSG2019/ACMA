from langchain_core.tools import tool
from math import sqrt, pi
from typing import Dict, Tuple, Union, List


@tool
def calculate_circle_area(radius: Union[int, float]) -> float:
    """
    Use this tool when you need to calculate the area of a circle given its radius.
    """
    return pi * radius ** 2

@tool
def calculate_pairwise_distances(haps_coords: List[List[Union[int, float]]]) -> str:
    """
    Use this tool when you need to calculate the distance between each pair of the four HAPS.
    The tool requires only one call
    """
    haps = ["HAPS0", "HAPS1", "HAPS2", "HAPS3"]
    distances = []

    for i in range(len(haps)):
        for j in range(i + 1, len(haps)):
            x1, y1 = haps_coords[i]
            x2, y2 = haps_coords[j]
            distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            distances.append(f"Distance between {haps[i]} and {haps[j]}: {distance:.2f} km")

    return "\n".join(distances)
