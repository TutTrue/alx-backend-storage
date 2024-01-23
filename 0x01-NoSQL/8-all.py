#!/usr/bin/env python3
""" list_all """


def list_all(mongo_collection) -> list:
    """list all documents in a collection"""
    return mongo_collection.find()
