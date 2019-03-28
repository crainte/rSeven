#!/usr/bin/env python3

from helpers.request import request

import json


GROUPS = dict()

def populate_groups():
    response = request.get('describe-security-groups')
    for group in response:
        if group['id'] not in GROUPS:
            # initialize the group entry
            GROUPS[group['id']] = dict()
            GROUPS[group['id']]['state'] = False
            GROUPS[group['id']]['depends'] = list()

        for ingress in group['ingress']:
            if 'cidr' in ingress and ingress['cidr'] == '0.0.0.0/0':
                GROUPS[group['id']]['state'] = True

            if 'sg' in ingress:
                GROUPS[group['id']]['depends'].append(ingress['sg'])


def classify_group(group):
    if GROUPS[group]['state']:
        return True

    for dep in GROUPS[group]['depends']:
        if classify_group(dep):
            return True
    return False

def classify_instances():
    response = request.get('describe-instances')
    for instance in response:
        open_to_world = False
        for group in instance['sg']:
            if classify_group(group):
                open_to_world = True
        if open_to_world:
            print("'%s' is open to world" % instance['id'])
        else:
            print("'%s' is not wide open" % instance['id'])


populate_groups()
for group in GROUPS:
    if classify_group(group):
        print("'%s' is open to the world" % group)
    else:
        print("'%s' is not wide open" % group)
classify_instances()
