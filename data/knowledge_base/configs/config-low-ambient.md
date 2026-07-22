---
id: configs/low-ambient-startup
name: "Configuration Profile — Low Ambient Startup"
type: config
description: "Recommended control setpoints and pre-heat profiles for low ambient starts to prevent oil migration and compressor damage."
severity: medium
tags: [config, startup, low-ambient]
---

# Low Ambient Startup Configuration Profile

Recommended settings:

- Crankcase heater test interval: monthly during winter
- Low ambient startup threshold: 40°F (configurable per asset)
- Minimum oil temperature before startup: 80°F for systems with prior oil-dilution events
- Startup pre-heat duration: 8–16 hours depending on ambient and oil condition

References:
- [[sops/sop-crankcase-heater]]
- [[components/crankcase-heater]]
- [[failures/103-prestart-temp-alert]]
