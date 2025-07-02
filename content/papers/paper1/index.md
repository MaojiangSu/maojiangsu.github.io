---
title: "Computational limits of low-rank adaptation (lora) for transformer-based models" 
date: 2025-04-24
tags: ["Fine-grained Complexity Theory","Transformers","Low-rank Adaptation","Computational Limits"]
author: ["Jerry Yao-Chieh Hu","Maojiang Su","En-Jui Kuo","Zhao Song","Han Liu"]
description: "We study the computational limits of Low-Rank Adaptation (LoRA) update for finetuning transformer-based models using fine-grained complexity theory. Published in the The International Conference on Learning Representations, 2025." 
summary: "We study the computational limits of Low-Rank Adaptation (LoRA) update for finetuning transformer-based models using fine-grained complexity theory. " 
cover:
    image: "paper1.png"
    alt: "Computational limits of low-rank adaptation (lora) for transformer-based models"
    relative: true
editPost:
    URL: "https://arxiv.org/abs/2406.03136"
    Text: "The International Conference on Learning Representations 2025"

---

---

##### Download

+ [Paper](theory_of_lora_iclr_2025.pdf)

---

##### Abstract

We study the computational limits of Low-Rank Adaptation (LoRA) update for finetuning transformer-based models using fine-grained complexity theory. Our key observation is that the existence of low-rank decompositions within the gradient computation of LoRA adaptation leads to possible algorithmic speedup. This allows us to (i) identify a phase transition behavior and (ii) prove the existence of nearly linear algorithms by controlling the LoRA update computation term by term, assuming the Strong Exponential Time Hypothesis (SETH).

---

##### Figure: Computational limits of low-rank adaptation (lora) for transformer-based models

![](paper1.png)
