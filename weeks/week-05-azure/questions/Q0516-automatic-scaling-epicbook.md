---
id: Q0516
title: Automatic Scaling of EpicBook in Azure
difficulty: medium
week: 05
topics: [azure, scaling, automation, architecture]
tags: [autoscale, load-balancer, performance, azure]
author: Whitney
reviewed: false
---

## Question
We've got an exciting problem - EpicBook is getting more popular! But yesterday, we had a blog post about us go viral, and suddenly our servers couldn't keep up with all the new users. Some people couldn't even log in because the system was so overwhelmed. I've heard Azure can automatically handle situations like this, but how exactly would that work with our web, app, and database setup? What do we need to set up to make sure this doesn't happen again?

## Short Answer
It's like having an automated restaurant manager who opens more registers when lines get long. Azure watches how busy EpicBook gets and automatically adds more servers when needed. The load balancer works like a traffic cop, directing users to the least busy servers. Even our database can grow or shrink based on demand. This keeps everything running smoothly even when lots of people show up at once.

## Deep Dive
Let's say it's a normal Tuesday morning and suddenly EpicBook gets featured on a popular tech blog. Traffic starts climbing fast. Here's what happens behind the scenes:

Azure App Service notices the CPU usage climbing past 70% and springs into action. It starts spinning up new instances of our app - maybe we normally run on 3 servers, but now we need 8 to handle all the traffic. The load balancer makes sure new users get sent to these new servers evenly.

Meanwhile, our database might be feeling the pressure too. If we're using Azure SQL, it can automatically scale up to handle more requests. The cool thing is, once the traffic dies down (maybe it's 3 AM and most users are asleep), Azure scales everything back down to save money. We only pay for what we actually need.

## Pitfalls
- Wrong autoscale metrics cause unnecessary scaling.  
- Missing cooldown periods trigger rapid scale-in/out loops.  
- No database scaling leads to bottlenecks.  
- Not testing load limits can cause app crashes under pressure.

## References
- https://learn.microsoft.com/en-us/azure/azure-monitor/autoscale/autoscale-overview
- https://learn.microsoft.com/en-us/azure/architecture/best-practices/auto-scaling