#
# Licensed under the MIT license. 
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the MIT license.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# 
# Written by John Keogh, 2025
#
import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="EyesBot MCP Server",
    instructions="When you are asked for the name of the robot or a description of its surroundings"
)


@mcp.tool()
def describe_surroundings() -> str:
    """Get the last surroundings noted by robot"""
    tool_url = get_url("getRobotSurroundings")
    return get_url_body(tool_url, False)


@mcp.tool()
def robot_name() -> str:
    """Get the name of the robot"""
    tool_url = get_url("getRobotName")
    return get_url_body(tool_url, False)


@mcp.resource("robot://camera/images/latest/", description="The most recent image captured by the robot's left or right camera.  Left is 0 and right is 1", mime_type="image/png")
def lastest_image() -> bytes:
    """Get most recent image captured by robot"""
    resource_url = get_url(f"image?camera=0")
    image_bytes = get_url_body(resource_url, True)
    return image_bytes


@mcp.prompt()
def get_robot_info() -> str:
    """Get information about robot"""
    return f"Could you get the robot's name and describe their surroundings"


def get_url(path):
    """
    Add the protocol part of the URL (HTTP(s)) and the base URL to the 
    passed in path and returns it
    """
    robot_base_url = os.environ['ROBOT_BASE_URL']
    protocol = "http" if (os.environ['SECURE_URL'] == "False") else "https"
    return f"{protocol}://{robot_base_url}/{path}"


def get_url_body(url, as_binary=False):
    """
    Makes a GET request to a given URL and returns the response body as text.
    Handles potential errors during the request.
    """
    try:
        response = requests.get(url)
        response.raise_for_status() 
        if as_binary:
            return response.content
        else:
            return response.text
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"ConnectionError: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout: {e}")
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
    return ""


if __name__ == "__main__":
    mcp.run()
