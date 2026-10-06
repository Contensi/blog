---
title: "VMware-Alternative Proxmox VE 9.2: Lohnt sich die Migration im Jahr 2026?"
date: 2026-07-28
author: "Nicola Anastassia"
description: "VMware wird für viele Unternehmen zunehmend kostspielig. Proxmox VE 9.2 bietet eine leistungsfähige Open-Source-Alternative. Erfahren Sie, welche Neuerungen die aktuelle Version mitbringt und wie eine erfolgreiche VMware-Migration geplant und umgesetzt wird."
summary: "VMware wird für viele Unternehmen zunehmend kostspielig. Proxmox VE 9.2 bietet eine leistungsfähige Open-Source-Alternative. Erfahren Sie, welche Neuerungen die aktuelle Version mitbringt und wie eine erfolgreiche VMware-Migration geplant und umgesetzt wird."
contact: daniel-heitmann
sources: "Proxmox Server Solutions GmbH, Pressemitteilung und Release Notes zu Proxmox VE 9.2 (Mai 2026)."
---

Proxmox VE 9.2 ist seit dem 21. Mai 2026 verfügbar - und bringt neben einem neuen Kernel vor allem ein Feature, das Cluster-Betrieb spürbar entspannt: den Dynamic Load Balancer. Ein Überblick, was die Version mitbringt und wofür sie sich lohnt.

## Dynamic Load Balancer: das größte Cluster-Feature seit den CRS-Regeln

Bisher entschied der Cluster Resource Scheduler (CRS) statisch, auf welchem Node eine HA-VM startet. Der neue Dynamic Load Balancer beobachtet CPU- und Memory-Auslastung laufend und verschiebt HA-Gäste aktiv, sobald ein Node aus der Balance gerät - ohne manuelles Eingreifen.

## Mehr Kontrolle über den HA-Stack

Der HA Manager lässt sich jetzt clusterweit „armieren" und „entwaffnen": Für geplante Wartungsfenster kann der HA-Stack vorübergehend ausgesetzt werden, damit er nicht versehentlich Nodes fenced, während gewartet wird.

## Netzwerk, Storage und Unterbau

- WireGuard als verschlüsseltes SDN-Fabric-Protokoll, IPv6-Underlay für EVPN
- Debian 13.5 „Trixie" als Basis, Kernel 7.0 als neuer Stable-Standard
- QEMU 11.0, LXC 7.0, ZFS 2.4
- Ceph Tentacle 20.2 jetzt stabil verfügbar, parallel zu Ceph Squid 19.2
- über fünfzig weitere Verbesserungen an VM-, Container-, Storage- und Backup-Stack

## Lohnt sich die Migration?

Für Umgebungen, die ohnehin gerade eine Alternative zu VMware evaluieren, macht 9.2 den Umstieg noch attraktiver: Der Dynamic Load Balancer und das flexible HA-Wartungsmanagement schließen zwei Lücken, die im praktischen Cluster-Betrieb bislang manuelle Nacharbeit bedeuteten. Ob sich ein Wechsel für Ihre konkrete Umgebung wirtschaftlich lohnt, hängt von Ihrer aktuellen Lizenzierung, der Anzahl Hosts und VMs sowie Ihrem gewünschten Zeitrahmen ab - dafür haben wir auf unserer [Proxmox-Seite](/proxmox) einen interaktiven Kostenrechner mit Rechenbeispiel für Ihre Umgebung hinterlegt.
