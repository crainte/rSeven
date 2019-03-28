#!/usr/bin/env python3

from helpers.request import request

import json


GROUPS = dict()
STATES = { 0: "initial state",
           1: "secure limit",
           2: "open to /24",
           3: "open to /8",
           99: "open to the world"}


def populate_groups():
    response = request.get('describe-security-groups')
    for group in response:
        if group['id'] not in GROUPS:
            # initialize the group entry
            GROUPS[group['id']] = dict()
            GROUPS[group['id']]['state'] = 0
            GROUPS[group['id']]['depends'] = list()

        for ingress in group['ingress']:
            # assign states to the different cidr types. Ideally you would use
            # python netaddr to actually calculate valid net addresses
            if 'cidr' in ingress and ingress['cidr'] == '0.0.0.0/0':
                GROUPS[group['id']]['state'] = 99
            elif 'cidr' in ingress and '/24' in ingress['cidr']:
                GROUPS[group['id']]['state'] = 2
            elif 'cidr' in ingress and '/8' in ingress['cidr']:
                GROUPS[group['id']]['state'] = 3
            elif 'cidr' in ingress and '/32' in ingress['cidr']:
                GROUPS[group['id']]['state'] = 1

            if 'sg' in ingress:
                GROUPS[group['id']]['depends'].append(ingress['sg'])


def classify_group(group):
    status = -1
    for dep in GROUPS[group]['depends']:
        temp = classify_group(dep)
        if temp > status:
            status = temp

    if GROUPS[group]['state'] > status:
        return GROUPS[group]['state']

    return status

def classify_instances():
    response = request.get('describe-instances')
    for instance in response:
        instance_state = -1
        for group in instance['sg']:
            temp = classify_group(group)
            if temp > instance_state:
                instance_state = temp

        print("'%s' is %s'" % (instance['id'], STATES[instance_state]))


populate_groups()
for group in GROUPS:
    print("'%s' is %s" % (group, STATES[classify_group(group)]))
classify_instances()
