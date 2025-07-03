---
title: "Fast and Low-Cost Genomic Foundation Models via Outlier Removal"
date: 2025-05-02
tags:
  ["Genomics", "Foundation Models", "Quantization", "LoRA", "Outlier Removal"]
author:
  [
    "Haozheng Luo",
    "Chenghao Qiu",
    "Maojiang Su",
    "Zhihan Zhou",
    "Zoe Mehta",
    "Guo Ye",
    "Jerry Yao-Chieh Hu",
    "Han Liu",
  ]
description: "This paper proposes GERM, an efficient genomic foundation model leveraging outlier removal techniques for low-cost fine-tuning and robust quantization. Published in the 42nd International Conference on Machine Learning (ICML), 2025."
summary: "GERM removes outliers to improve genomic model efficiency, enabling quantization and LoRA fine-tuning with minimal degradation."
cover:
  image: "germ_icml2025_poster.png"
  alt: "GERM: Fast and Low-Cost Genomic Foundation Models"
  relative: true
editPost:
  URL: "https://github.com/MAGICS-LAB/GERM"
  Text: "Published in the 42nd International Conference on Machine Learning (ICML), 2025."
---

##### Download

- [Paper (PDF)](Fast%20and%20Low-Cost%20Genomic%20Foundation%20Models%20via%20Outlier%20Removal.pdf)

---

##### Abstract

To address the challenge of scarce computational resources in genomic modeling, this paper introduces **GERM**, a genomic foundation model with strong compression performance and fast adaptability. GERM eliminates outliers during both pretraining and fine-tuning stages, enhancing both LoRA-based low-rank adaptation and post-training quantization robustness. Additionally, a continual learning variant named **GERM-T** further reduces retraining costs by applying outlier removal in small steps. Compared to DNABERT-2, GERM improves fine-tuning performance by **37.98%**, quantization robustness by **64.34%**, and reduces average kurtosis by **92.14%**. These results demonstrate GERM’s practical effectiveness for genomic tasks in resource-constrained environments.

---

##### Figure

![](germ_icml2025_poster.png)
