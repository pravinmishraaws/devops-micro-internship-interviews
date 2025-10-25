---
id: Q0517
title: Azure Virtual Networks — secure communication architecture
difficulty: medium
week: 05
topics: [azure, networking, security]
tags: [azure, vnet, networking, hybrid-cloud]
author: "[Dudubynatur3](https://github.com/Dudubynatur3)"
reviewed: false
---

## Question
Can you explain what an Azure Virtual Network (VNet) is and how it enables secure communication between Azure resources and on-premises environments?

## Short Answer
- Azure VNet is an isolated network in Azure for resource communication.
- Enables secure connectivity via VPN Gateway or ExpressRoute to on-premises.
- Provides subnetting, NSGs (Network Security Groups), and private IPs.
- Resources in same VNet can communicate; cross-VNet needs peering or gateway.

## Deep Dive
- **VNet components:** Address space (CIDR), subnets, NSGs, route tables.
- **On-premises connectivity:**
  - Site-to-Site VPN: Encrypted tunnel over internet.
  - ExpressRoute: Private dedicated connection (higher cost, better performance).
  - Point-to-Site VPN: Individual client access.
- **Security:** NSGs act as firewalls; Service Endpoints keep traffic on Azure backbone.
- **Peering:** VNet-to-VNet connectivity (same region or global) with low latency.
- **Use cases:** Multi-tier apps, hybrid workloads, Azure-to-on-prem databases.

## Pitfalls
- Overlapping CIDR ranges prevent peering or VPN setup.
- Forgetting to configure NSG rules blocks legitimate traffic.
- ExpressRoute requires upfront planning (not instant setup like VPN).
- Default Azure DNS may not resolve on-prem hostnames (need custom DNS).

## References
- https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview
- https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways
- https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction
