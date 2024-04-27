# Create Wait Time Functions

This last capability your chatbot needs is to answer questions about hospital wait times. As discussed earlier, your organization doesn’t store wait time data anywhere, so your chatbot will have to fetch it from an external source. You’ll write two functions for this—one that simulates finding the current wait time at a hospital, and another that finds the hospital with the shortest wait time.

**Note:** The purpose of creating wait time functions is to show you that LangChain agents can run arbitrary Python code, not just chains or other LangChain methods. This capability is extremely valuable because it means, in theory, you could create an agent to do just about anything that can be expressed in code.

Start by defining functions to fetch current wait times at a hospital:

```python
import os
from typing import Any
import dotenv

import numpy as np
from langchain_community.graphs import Neo4jGraph

dotenv.load_dotenv()


def _get_current_hospitals() -> list[str]:
    """Fetch a list of current hospital names from a Neo4j database."""
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
    )

    current_hospitals = graph.query(
        """
        MATCH (h:Hospital)
        RETURN h.name AS hospital_name
        """
    )

    current_hospitals = [d["hospital_name"].lower() for d in current_hospitals]

    return current_hospitals


def _get_current_wait_time_minutes(hospital: str) -> int:
    """Get the current wait time at a hospital in minutes."""

    current_hospitals = _get_current_hospitals()

    if hospital.lower() not in current_hospitals:
        return -1

    return np.random.randint(low=0, high=600)


def get_current_wait_times(hospital: str) -> str:
    """Get the current wait time at a hospital formatted as a string."""

    wait_time_in_minutes = _get_current_wait_time_minutes(hospital)

    if wait_time_in_minutes == -1:
        return f"Hospital '{hospital}' does not exist."

    hours, minutes = divmod(wait_time_in_minutes, 60)

    if hours > 0:
        formatted_wait_time = f"{hours} hours {minutes} minutes"
    else:
        formatted_wait_time = f"{minutes} minutes"

    return formatted_wait_time


def get_most_available_hospital(_: Any) -> dict[str, float]:
    """Find the hospital with the shortest wait time."""

    current_hospitals = _get_current_hospitals()

    current_wait_times = [_get_current_wait_time_minutes(h) for h in current_hospitals]

    best_time_idx = np.argmin(current_wait_times)
    best_hospital = current_hospitals[best_time_idx]
    best_wait_time = current_wait_times[best_time_idx]

    return {best_hospital: best_wait_time}


```

The first function you define is \_get_current_hospitals() which returns a list of hospital names from your Neo4j database. Then, \_get_current_wait_time_minutes() takes a hospital name as input. If the hospital name is invalid, \_get_current_wait_time_minutes() returns -1. If the hospital name is valid, \_get_current_wait_time_minutes() returns a random integer between 0 and 600 simulating a wait time in minutes.

You then define get_current_wait_times() which is a wrapper around \_get_current_wait_time_minutes() that returns the wait time formatted as a string.

You can use \_get_current_wait_time_minutes() to define a second function that finds the hospital with the shortest wait time:

```python

# ...

def get_most_available_hospital(_: Any) -> dict[str, float]:
    """Find the hospital with the shortest wait time."""
    current_hospitals = _get_current_hospitals()

    current_wait_times = [
        _get_current_wait_time_minutes(h) for h in current_hospitals
    ]

    best_time_idx = np.argmin(current_wait_times)
    best_hospital = current_hospitals[best_time_idx]
    best_wait_time = current_wait_times[best_time_idx]

    return {best_hospital: best_wait_time}

```

Here, you define get\*most*available_hospital() which calls \_get_current_wait_time_minutes() on each hospital and returns the hospital with the shortest wait time. Notice how get_most_available_hospital() has a [throwaway input](https://realpython.com/python-double-underscore/#public-interfaces-and-naming-conventions-in-python)*. This will be required later on by your agent because it’s designed to pass inputs into functions.

Here’s how you use get_current_wait_times() and get_most_available_hospital():

```python
import dotenv

dotenv.load_dotenv()


from wait_times import (
    get_current_wait_times,
    get_most_available_hospital,
)

print(get_current_wait_times("Wallace-Hamilton"))


print(get_current_wait_times("fake hospital"))


print(get_most_available_hospital(None))

```

After loading environment variables, you call get_current_wait_times("Wallace-Hamilton") which returns the current wait time in minutes at **Wallace-Hamilton** hospital. When you try get_current_wait_times("fake hospital"), you get a string telling you **fake hospital** does not exist in the database.

Lastly, get_most_available_hospital() returns a dictionary storing the wait time for the hospital with the shortest wait time in minutes. Next, you’ll create an agent that uses these functions, along with the Cypher and review chain, to answer arbitrary questions about the hospital system.
