---
id: Q0514
title: Safe Software Rollouts with Azure Canary Deployments
difficulty: medium
week: 05
topics: [azure, deployment, devops, testing]
tags: [canary, rollout, updates, monitoring]
author: Whitney
reviewed: false
---

## Question
So we've got this exciting new feature for EpicBook that we want to release, but last time we pushed an update, we had some unexpected issues that affected all our users at once. Ouch! I've packaged the new feature as a container image, but I'm nervous about rolling it out to everyone immediately. Is there a way we can test it with just a small group of users first? You know, like a "soft launch" to make sure everything's working properly before we go all in?

## Short Answer
Think of canary deployments like a taste test. Instead of serving a new recipe to everyone at once, we let a small group try it first. With EpicBook, we'll roll out new features to maybe 5% of our users initially. We watch how it performs and gather feedback. If everything looks good, we gradually serve it to more users. This way, if something's not quite right, we've only affected a small group, not everyone.

## Deep Dive
The name "canary deployment" comes from the old coal mining practice - miners would bring canaries into mines to detect dangerous gases. In our case, we're using a small group of servers or users to detect potential problems with new code.

We use Azure DevOps to manage this process. It's pretty clever - we can say "send 10% of our traffic to the new version" and Azure's Traffic Manager handles all the routing. The whole time, we're watching our monitoring tools like hawks - checking error rates, response times, and user behavior. If anything looks off, we can quickly flip a switch and send everyone back to the previous version that we know works well.

## Pitfalls
- Skipping monitoring means you may miss early failures.  
- Poor traffic routing setup may send too many users to the canary release.  
- Not testing rollback scripts can delay recovery.  
- Missing user segmentation can give unclear results.

## References
- https://learn.microsoft.com/en-us/azure/devops/pipelines/deploy/canary-deployments
- https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-overview