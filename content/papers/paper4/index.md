---
title: "High-Order Flow Matching: Unified Framework and Sharp Statistical Rates" 
date: 2025-09-18
tags: ["Flow Matching","Transformers","Statistical Rates","High-Order Dynamics"]
author: ["Maojiang Su","Jerry Yao-Chieh Hu","Yi-Chen Lee","Ning Zhu","Jui-Hui Chung","Shang Wu","Zhao Song","Minshuo Chen","Han Liu"]
description: "We present a unified framework for standard and high-order flow matching that incorporates trajectory derivatives up to an arbitrary order $K$. Our key innovation is establishing the marginalization technique that converts the intractable $K$-order loss into a simple conditional regression with exact gradients and identifying the consistency constraint. We establish sharp statistical rates of the $K$-order flow matching implemented with transformer networks. " 
cover:
    image: "high_order_FM_ver_prelim.pdf"
    alt: "High-Order Flow Matching: Unified Framework and Sharp Statistical Rates"
    relative: true
editPost:
    URL: "https://arxiv.org/abs/2406.03136"
    Text: "Neural Information Processing Systems 2025"

---

---

##### Download

+ [Paper](high_order_FM_ver_prelim.pdf)

---

##### Abstract

Flow matching is an emerging generative modeling framework that learns continuous-time dynamics to map noise into data. To enhance expressiveness and sampling efficiency, recent works have explored incorporating high-order trajectory information. Despite the empirical success, a holistic theoretical foundation is still lacking. We present a unified framework for standard and high-order flow matching that incorporates trajectory derivatives up to an arbitrary order $K$. Our key innovation is establishing the marginalization technique that converts the intractable $K$-order loss into a simple conditional regression with exact gradients and identifying the consistency constraint. We establish sharp statistical rates of the $K$-order flow matching implemented with transformer networks. With $n$ samples, flow matching estimates nonparametric distributions at a rate $\tilde{O}(n^{-\Theta(1/d)})$, matching minimax lower bounds up to logarithmic factors.

---

##### Figure: Computational limits of low-rank adaptation (lora) for transformer-based models

![](paper4.jpeg)
