---
title: "VMware alternative Proxmox VE 9.2: Is migrating worth it in 2026?"
date: 2026-07-28
author: "Nicola Anastassia"
description: "VMware is becoming increasingly costly for many companies. Proxmox VE 9.2 offers a capable open-source alternative. Find out what’s new in the current version and how to plan and execute a successful VMware migration."
summary: "VMware is becoming increasingly costly for many companies. Proxmox VE 9.2 offers a capable open-source alternative. Find out what’s new in the current version and how to plan and execute a successful VMware migration."
contact: daniel-heitmann
sources: "Proxmox Server Solutions GmbH, press release and release notes for Proxmox VE 9.2 (May 2026)."
---

Proxmox VE 9.2 has been available since 21 May 2026 - and alongside a new kernel, it brings one feature in particular that noticeably eases cluster operations: the Dynamic Load Balancer. Here’s what’s new in this release and where it pays off.

## Dynamic Load Balancer: the biggest cluster feature since CRS rules

Until now, the Cluster Resource Scheduler (CRS) decided statically where an HA guest would start. The new Dynamic Load Balancer continuously monitors CPU and memory pressure and actively migrates HA guests once a node falls out of balance - no manual intervention needed.

## More control over the HA stack

The HA Manager can now be "armed" and "disarmed" cluster-wide: for planned maintenance windows, the HA stack can be temporarily suspended so it doesn’t accidentally fence nodes while work is being carried out.

## Networking, storage and the underlying platform

- WireGuard as an encrypted SDN fabric protocol, IPv6 underlay for EVPN
- Debian 13.5 "Trixie" as the base, kernel 7.0 as the new stable default
- QEMU 11.0, LXC 7.0, ZFS 2.4
- Ceph Tentacle 20.2 now available as stable, alongside Ceph Squid 19.2
- more than fifty further improvements across the VM, container, storage and backup stack

## Is migrating worth it?

For environments already evaluating alternatives to VMware, 9.2 makes the switch even more attractive: the Dynamic Load Balancer and flexible HA maintenance management close two gaps that previously meant manual follow-up work in day-to-day cluster operations. Whether a switch pays off economically for your specific environment depends on your current licensing, the number of hosts and VMs, and your desired timeframe - which is exactly why our [Proxmox page](/proxmox-en) has an interactive cost calculator with a worked example for your environment.
