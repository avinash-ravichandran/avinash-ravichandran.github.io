// ============================================================
//  Single source of truth. Edit this file to update the site.
// ============================================================

window.SITE_DATA = {
  profile: {
    name: "Avinash Ravichandran",
    location: "Seattle",
    role: "Principal Applied Scientist",
    org: "Amazon",
    headshot: "https://avinash-ravichandran.github.io/images/avinash-headshot.JPG",
    links: {
      scholar: "https://scholar.google.com/citations?hl=en&user=28p_eLYAAAAJ",
      amazonScience: "https://www.amazon.science/author/avinash-ravichandran",
      linkedin: "https://www.linkedin.com/in/avinash-ravichandran-2933a8b"
    },
    bio: [
      "I work on multimodal foundation models: how they learn, how they adapt, and how they run in production. That spans vision-language understanding, generative models, efficient transfer and fine-tuning, and the infrastructure that makes any of it practical.",
      "I'm currently a Principal Applied Scientist at Amazon. Before rejoining, I was Chief Architect of Machine Learning at SambaNova Systems, shaping multimodal AI for their hardware stack. Earlier, I was a Principal Scientist at Cruise bringing foundation models into AV perception, and I spent nearly a decade at Amazon helping launch large-scale ML products including AWS Rekognition Custom Labels.",
      "I earned my PhD in Electrical and Computer Engineering from Johns Hopkins University under Dr. René Vidal, and completed a postdoctoral fellowship at UCLA with Dr. Stefano Soatto."
    ]
  },

  // Selected publications — referenced by exact title match against the publications list below.
  selected: [
    "Training Domain Draft Models for Speculative Decoding",
    "WinCLIP: Zero-/Few-Shot Anomaly Classification and Segmentation",
    "X-DETR: A Versatile Architecture for Instance-wise Vision-Language Tasks",
    "Task Adaptive Parameter Sharing for Multi-task Learning",
    "Meta-Learning with Differentiable Convex Optimization",
    "Task2Vec: Task Embedding for Meta-Learning",
    "Few-Shot Learning with Embedded Class Models and Shot-Free Meta Training",
    "Categorizing Dynamic Textures using a Bag of Dynamical Systems"
  ],

  // Topic taxonomy — keys used by publications below
  topics: {
    "few-shot":   { label: "Few-shot",           color: "#8a5a3c" },
    "continual":  { label: "Continual learning", color: "#3c5a8a" },
    "vlm":        { label: "Vision-language",    color: "#6a3c8a" },
    "meta":       { label: "Meta-learning",      color: "#3c8a5a" },
    "finetune":   { label: "Fine-tuning",        color: "#8a3c5a" },
    "dynamical":  { label: "Dynamical systems",  color: "#5a8a3c" },
    "detection":  { label: "Detection/Seg",      color: "#8a7a3c" },
    "ssl":        { label: "Self/Semi-sup",      color: "#3c8a8a" },
    "systems":    { label: "ML systems",         color: "#444444" }
  },

  publications: [
    // 2025
    { y: 2025, type: "preprint", t: "Training Domain Draft Models for Speculative Decoding", v: "arXiv:2503.07807", a: ["Fenglu Hong","Ravi Raju","Jonathan Lingjie Li","Bo Li","Urmish Thakker","A. Ravichandran","Swayambhoo Jain","Changran Hu"], url: "https://arxiv.org/abs/2503.07807", tags: ["systems","finetune"] },
    { y: 2025, type: "preprint", t: "Fine Tuning without Catastrophic Forgetting via Selective Low Rank Adaptation", v: "arXiv", a: ["R. Akbarian Bafghi","C. Bagwell","A. Ravichandran","A. Shrivastava","M. Raissi"], url: "https://ui.adsabs.harvard.edu/abs/2025arXiv250115377A/abstract", tags: ["finetune","continual"] },

    // 2024
    { y: 2024, type: "preprint", t: "VLM-KD: Knowledge Distillation from VLM for Long-Tail Visual Recognition", v: "arXiv:2408.16930", a: ["Z. Zhang","G. P. Meyer","Z. Lu","A. Shrivastava","A. Ravichandran","E. M. Wolff"], url: "https://arxiv.org/abs/2408.16930", tags: ["vlm","detection"] },
    { y: 2024, type: "preprint", t: "InVi: Object Insertion in Videos using Off-the-Shelf Diffusion Models", v: "arXiv:2407.10958", a: ["N. Saini","N. Bodla","A. Shrivastava","A. Ravichandran","X. Zhang","A. Shrivastava","B. Singh"], url: "https://arxiv.org/abs/2407.10958", tags: ["vlm"] },
    { y: 2024, type: "preprint", t: "GenMM: Geometrically and Temporally Consistent Multimodal Data Generation for Video and LiDAR", v: "arXiv:2406.10722", a: ["B. Singh","V. Kulharia","L. Yang","A. Ravichandran","A. Tyagi","A. Shrivastava"], url: "https://arxiv.org/abs/2406.10722", tags: ["vlm","detection"] },
    { y: 2024, type: "preprint", t: "CLAP: Unsupervised 3D Representation Learning for Fusion 3D Perception", v: "arXiv:2412.03059", a: ["R. Chen","H. Zhang","A. Ravichandran","H. Park","W. Shao","A. Wong","P. Luo"], url: "https://arxiv.org/abs/2412.03059", tags: ["ssl","detection"] },

    // 2023
    { y: 2023, type: "conf", t: "Your representations are in the network: composable and parallel adaptation for large scale models", v: "NeurIPS", a: ["Y. Dukler","A. Achille","H. Yang","V. Vivek","L. Zancato","B. Bowman","A. Ravichandran","C. Fowlkes","A. Swaminathan","S. Soatto"], url: "https://proceedings.neurips.cc/paper_files/paper/2023/hash/5be3783ea9d43d7add5409c101d87d83-Abstract-Conference.html", tags: ["finetune"] },
    { y: 2023, type: "conf", t: "WinCLIP: Zero-/Few-Shot Anomaly Classification and Segmentation", v: "CVPR", a: ["J. Jeong","Y. Zou","T. Kim","D. Zhang","A. Ravichandran","O. Dabeer"], url: "http://openaccess.thecvf.com/content/CVPR2023/html/Jeong_WinCLIP_Zero-Few-Shot_Anomaly_Classification_and_Segmentation_CVPR_2023_paper.html", tags: ["vlm","few-shot","detection"] },
    { y: 2023, type: "conf", t: "Learning Expressive Prompting with Residuals for Vision Transformers", v: "CVPR", a: ["R. Das","Y. Dukler","A. Ravichandran","A. Swaminathan"], url: "http://openaccess.thecvf.com/content/CVPR2023/html/Das_Learning_Expressive_Prompting_With_Residuals_for_Vision_Transformers_CVPR_2023_paper.html", tags: ["finetune"] },
    { y: 2023, type: "conf", t: "A Meta-Learning Approach to Predicting Performance and Data Requirements", v: "CVPR", a: ["A. Jain","G. Swaminathan","P. Favaro","H. Yang","A. Ravichandran","H. Harutyunyan","A. Achille","O. Dabeer","B. Schiele","A. Swaminathan","S. Soatto"], url: "http://openaccess.thecvf.com/content/CVPR2023/html/Jain_A_Meta-Learning_Approach_to_Predicting_Performance_and_Data_Requirements_CVPR_2023_paper.html", tags: ["meta"] },
    { y: 2023, type: "journal", t: "Introspective Cross-Attention Probing for Lightweight Transfer of Pre-trained Models", v: "CoRR", a: ["Y. Dukler","A. Achille","H. Yang","V. Vivek","L. Zancato","B. Bowman","A. Ravichandran","C. Fowlkes","A. Swaminathan","S. Soatto"], url: "https://openreview.net/forum?id=W4tJkscoAI", tags: ["finetune"] },

    // 2022
    { y: 2022, type: "conf", t: "X-DETR: A Versatile Architecture for Instance-wise Vision-Language Tasks", v: "ECCV", a: ["Z. Cai","G. Kwon","A. Ravichandran","E. Bas","Z. Tu","R. Bhotika","S. Soatto"], url: "https://link.springer.com/chapter/10.1007/978-3-031-20059-5_17", tags: ["vlm","detection"] },
    { y: 2022, type: "conf", t: "Task Adaptive Parameter Sharing for Multi-task Learning", v: "CVPR", a: ["M. Wallingford","H. Li","A. Achille","A. Ravichandran","C. Fowlkes","R. Bhotika","S. Soatto"], url: "http://openaccess.thecvf.com/content/CVPR2022/html/Wallingford_Task_Adaptive_Parameter_Sharing_for_Multi-Task_Learning_CVPR_2022_paper.html", tags: ["finetune"] },
    { y: 2022, type: "conf", t: "Semi-supervised Vision Transformers at Scale", v: "NeurIPS", a: ["Z. Cai","A. Ravichandran","P. Favaro","M. Wang","D. Modolo","R. Bhotika","Z. Tu","S. Soatto"], url: "https://proceedings.neurips.cc/paper_files/paper/2022/hash/a4a1ee071ce0fe63b83bce507c9dc4d7-Abstract-Conference.html", tags: ["ssl"] },
    { y: 2022, type: "conf", t: "Rethinking Few-shot Object Detection on a Multi-Domain Benchmark", v: "ECCV", a: ["K. Lee","H. Yang","S. Chakraborty","Z. Cai","G. Swaminathan","A. Ravichandran","O. Dabeer"], url: "https://link.springer.com/chapter/10.1007/978-3-031-20044-1_21", tags: ["few-shot","detection"] },
    { y: 2022, type: "conf", t: "Class-incremental Learning with Strong Pre-trained Models", v: "CVPR", a: ["T.-Y. Wu","G. Swaminathan","Z. Li","A. Ravichandran","N. Vasconcelos","R. Bhotika","S. Soatto"], url: "http://openaccess.thecvf.com/content/CVPR2022/html/Wu_Class-Incremental_Learning_With_Strong_Pre-Trained_Models_CVPR_2022_paper.html", tags: ["continual"] },
    { y: 2022, type: "preprint", t: "Masked Vision and Language Modeling for Multi-modal Representation Learning", v: "arXiv:2208.02131", a: ["G. Kwon","Z. Cai","A. Ravichandran","E. Bas","R. Bhotika","S. Soatto"], url: "https://arxiv.org/abs/2208.02131", tags: ["vlm","ssl"] },
    { y: 2022, type: "preprint", t: "Completr: Reducing the Cost of Annotations for Object Detection in Dense Scenes", v: "arXiv:2209.05654", a: ["A. Jain","K. Lee","G. Swaminathan","H. Yang","B. Schiele","A. Ravichandran","O. Dabeer"], url: "https://arxiv.org/abs/2209.05654", tags: ["detection"] },

    // 2021
    { y: 2021, type: "conf", t: "Uniform Sampling over Episode Difficulty", v: "NeurIPS", a: ["S. Arnold","G. Dhillon","A. Ravichandran","S. Soatto"], url: "https://proceedings.neurips.cc/paper/2021/hash/0b3f44d9054402de39441e165a4bdfe0-Abstract.html", tags: ["meta","few-shot"] },
    { y: 2021, type: "conf", t: "Mixed-Privacy Forgetting in Deep Networks", v: "CVPR", a: ["A. Golatkar","A. Achille","A. Ravichandran","M. Polito","S. Soatto"], url: "http://openaccess.thecvf.com/content/CVPR2021/html/Golatkar_Mixed-Privacy_Forgetting_in_Deep_Networks_CVPR_2021_paper.html", tags: ["continual"] },
    { y: 2021, type: "conf", t: "LQF: Linear Quadratic Fine-Tuning", v: "CVPR", a: ["A. Achille","A. Golatkar","A. Ravichandran","M. Polito","S. Soatto"], url: "http://openaccess.thecvf.com/content/CVPR2021/html/Achille_LQF_Linear_Quadratic_Fine-Tuning_CVPR_2021_paper.html", tags: ["finetune"] },
    { y: 2021, type: "conf", t: "Exponential Moving Average Normalization for Self-/Semi-supervised Learning", v: "CVPR", a: ["Z. Cai","A. Ravichandran","S. Maji","C. Fowlkes","Z. Tu","S. Soatto"], url: "http://openaccess.thecvf.com/content/CVPR2021/html/Cai_Exponential_Moving_Average_Normalization_for_Self-Supervised_and_Semi-Supervised_Learning_CVPR_2021_paper.html", tags: ["ssl"] },
    { y: 2021, type: "preprint", t: "Supervised Momentum Contrastive Learning for Few-Shot Classification", v: "arXiv:2101.11058", a: ["O. Majumder","A. Ravichandran","S. Maji","A. Achille","M. Polito","S. Soatto"], url: "https://arxiv.org/abs/2101.11058", tags: ["few-shot","ssl"] },
    { y: 2021, type: "preprint", t: "Revisiting Contrastive Learning for Few-Shot Classification", v: "arXiv", a: ["O. Majumder","A. Ravichandran","S. Maji","M. Polito","R. Bhotika","S. Soatto"], url: "#", tags: ["few-shot","ssl"] },
    { y: 2021, type: "preprint", t: "Representation Consolidation for Training Expert Students", v: "arXiv:2107.08039", a: ["Z. Li","A. Ravichandran","C. Fowlkes","M. Polito","R. Bhotika","S. Soatto"], url: "https://arxiv.org/abs/2107.08039", tags: ["finetune"] },
    { y: 2021, type: "preprint", t: "Estimating Informativeness of Samples with Smooth Unique Information", v: "arXiv:2101.06640", a: ["H. Harutyunyan","A. Achille","G. Paolini","O. Majumder","A. Ravichandran","R. Bhotika","S. Soatto"], url: "https://arxiv.org/abs/2101.06640", tags: ["meta"] },
    { y: 2021, type: "preprint", t: "DIVA: Dataset Derivative of a Learning Task", v: "arXiv:2111.09785", a: ["Y. Dukler","A. Achille","G. Paolini","A. Ravichandran","M. Polito","S. Soatto"], url: "https://arxiv.org/abs/2111.09785", tags: ["meta"] },
    { y: 2021, type: "preprint", t: "A Linearized Framework and a New Benchmark for Model Selection for Fine-Tuning", v: "arXiv:2102.00084", a: ["A. Deshpande","A. Achille","A. Ravichandran","H. Li","L. Zancato","C. Fowlkes","R. Bhotika","S. Soatto","P. Perona"], url: "https://arxiv.org/abs/2102.00084", tags: ["finetune","meta"] },

    // 2020
    { y: 2020, type: "conf", t: "Predicting Training Time Without Training", v: "NeurIPS", a: ["L. Zancato","A. Achille","A. Ravichandran","R. Bhotika","S. Soatto"], url: "https://proceedings.neurips.cc/paper/2020/hash/440e7c3eb9bbcd4c33c3535354a51605-Abstract.html", tags: ["meta","systems"] },
    { y: 2020, type: "conf", t: "Incremental Few-Shot Meta-Learning via Indirect Discriminant Alignment", v: "ECCV", a: ["Q. Liu","O. Majumder","A. Achille","A. Ravichandran","R. Bhotika","S. Soatto"], url: "https://link.springer.com/chapter/10.1007/978-3-030-58571-6_40", tags: ["few-shot","continual","meta"] },
    { y: 2020, type: "conf", t: "A Baseline for Few-Shot Image Classification", v: "ICLR", a: ["G. S. Dhillon","P. Chaudhari","A. Ravichandran","S. Soatto"], url: "https://openreview.net/forum?id=rylXBkrYDS", tags: ["few-shot"] },
    { y: 2020, type: "preprint", t: "Rethinking the Hyperparameters for Fine-tuning", v: "arXiv:2002.11770", a: ["H. Li","P. Chaudhari","H. Yang","M. Lam","A. Ravichandran","R. Bhotika","S. Soatto"], url: "https://arxiv.org/abs/2002.11770", tags: ["finetune"] },
    { y: 2020, type: "preprint", t: "Multi-task Incremental Learning for Object Detection", v: "arXiv:2002.05347", a: ["X. Liu","H. Yang","A. Ravichandran","R. Bhotika","S. Soatto"], url: "https://arxiv.org/abs/2002.05347", tags: ["continual","detection"] },

    // 2019
    { y: 2019, type: "conf", t: "Task2Vec: Task Embedding for Meta-Learning", v: "ICCV", a: ["A. Achille","M. Lam","R. Tewari","A. Ravichandran","S. Maji","C. C. Fowlkes","S. Soatto","P. Perona"], url: "http://openaccess.thecvf.com/content_ICCV_2019/html/Achille_Task2Vec_Task_Embedding_for_Meta-Learning_ICCV_2019_paper.html", tags: ["meta"] },
    { y: 2019, type: "conf", t: "Meta-Learning with Differentiable Convex Optimization", v: "CVPR", a: ["K. Lee","S. Maji","A. Ravichandran","S. Soatto"], url: "http://openaccess.thecvf.com/content_CVPR_2019/html/Lee_Meta-Learning_With_Differentiable_Convex_Optimization_CVPR_2019_paper.html", tags: ["meta","few-shot"] },
    { y: 2019, type: "conf", t: "Few-Shot Learning with Embedded Class Models and Shot-Free Meta Training", v: "ICCV", a: ["A. Ravichandran","R. Bhotika","S. Soatto"], url: "http://openaccess.thecvf.com/content_ICCV_2019/html/Ravichandran_Few-Shot_Learning_With_Embedded_Class_Models_and_Shot-Free_Meta_Training_ICCV_2019_paper.html", tags: ["few-shot","meta"] },
    { y: 2019, type: "preprint", t: "Unbiased Evaluation of Deep Metric Learning Algorithms", v: "arXiv:1911.12528", a: ["I. Fehervari","A. Ravichandran","S. Appalaraju"], url: "https://arxiv.org/abs/1911.12528", tags: ["meta"] },

    // 2014
    { y: 2014, type: "conf", t: "Active Frame, Location, and Detector Selection for Automated and Manual Video Annotation", v: "CVPR (Tech Rep.)", a: ["V. Karasev","A. Ravichandran","S. Soatto"], url: "https://www.cv-foundation.org/openaccess/content_cvpr_2014/html/Karasev_Active_Frame_Location_2014_CVPR_paper.html", tags: ["detection"] },
    { y: 2014, type: "journal", t: "Dynamical Systems in Video Analysis", v: "Elsevier", a: ["G. Doretto","A. Ravichandran","R. Vidal","S. Soatto"], url: "https://www.sciencedirect.com/science/article/pii/B9780123965011000169", tags: ["dynamical"] },

    // 2013
    { y: 2013, type: "conf", t: "Semantic Video Segmentation from Occlusion Relations within a Convex Optimization Framework", v: "Springer", a: ["B. Taylor","A. Ayvaci","A. Ravichandran","S. Soatto"], url: "https://link.springer.com/chapter/10.1007/978-3-642-40395-8_15", tags: ["detection","dynamical"] },

    // 2012
    { y: 2012, type: "conf", t: "Superfloxels: A Mid-Level Representation for Video Sequences", v: "ECCV Workshops", a: ["A. Ravichandran","C. Wang","M. Raptis","S. Soatto"], url: "https://link.springer.com/chapter/10.1007/978-3-642-33885-4_14", tags: ["dynamical"] },
    { y: 2012, type: "conf", t: "Long-Range Spatio-Temporal Modeling of Video with Application to Fire Detection", v: "Springer", a: ["A. Ravichandran","S. Soatto"], url: "https://link.springer.com/chapter/10.1007/978-3-642-33709-3_24", tags: ["dynamical","detection"] },
    { y: 2012, type: "conf", t: "Image Priors for Image Deblurring with Uncertain Blur", v: "BMVC", a: ["D. Perrone","A. Ravichandran","R. Vidal","P. Favaro"], url: "https://home.inf.unibe.ch/~cvg/dperrone/uncertainblur/PerroneEtalBMVC2012.pdf", tags: ["dynamical"] },
    { y: 2012, type: "conf", t: "Group Action Induced Distances for Averaging and Clustering Linear Dynamical Systems", v: "CVPR", a: ["B. Afsari","R. Chaudhry","A. Ravichandran","R. Vidal"], url: "https://ieeexplore.ieee.org/abstract/document/6247929/", tags: ["dynamical"] },
    { y: 2012, type: "conf", t: "Encoding Scene Structures for Video Compression", v: "SPIE", a: ["G. Georgiadis","A. Ravichandran","S. Soatto","A. Chiuso"], url: "https://www.spiedigitallibrary.org/conference-proceedings-of-spie/8499/84991G/Encoding-scene-structures-for-video-compression/10.1117/12.930318.short", tags: ["dynamical"] },
    { y: 2012, type: "journal", t: "Categorizing Dynamic Textures using a Bag of Dynamical Systems", v: "IEEE TPAMI", a: ["A. Ravichandran","R. Chaudhry","R. Vidal"], url: "https://ieeexplore.ieee.org/abstract/document/6178260/", tags: ["dynamical"] },

    // 2011
    { y: 2011, type: "conf", t: "A Closed Form Solution to Robust Subspace Estimation and Clustering", v: "CVPR", a: ["P. Favaro","R. Vidal","A. Ravichandran"], url: "https://ieeexplore.ieee.org/abstract/document/5995365/", tags: ["dynamical"] },

    // 2010
    { y: 2010, type: "thesis", t: "Categorizing Video Sequences of Non-Rigid Dynamical Objects", v: "PhD Thesis, JHU", a: ["A. A. Ravichandran"], url: "https://search.proquest.com/openview/1c0fa8cc572a31b0d2514da6a009789f/1?pq-origsite=gscholar&cbl=18750", tags: ["dynamical"] },
    { y: 2010, type: "conf", t: "A Unified Approach to Segmentation and Categorization of Dynamic Textures", v: "Springer", a: ["A. Ravichandran","P. Favaro","R. Vidal"], url: "https://link.springer.com/chapter/10.1007/978-3-642-19315-6_33", tags: ["dynamical","detection"] },

    // 2009
    { y: 2009, type: "conf", t: "View-Invariant Dynamic Texture Recognition using a Bag of Dynamical Systems", v: "CVPR", a: ["A. Ravichandran","R. Chaudhry","R. Vidal"], url: "https://ieeexplore.ieee.org/abstract/document/5206847/", tags: ["dynamical"] },
    { y: 2009, type: "conf", t: "Histograms of Oriented Optical Flow and Binet-Cauchy Kernels for Action Recognition", v: "IEEE", a: ["R. Chaudhry","A. Ravichandran","G. Hager","R. Vidal"], url: "https://ieeexplore.ieee.org/abstract/document/5206821/", tags: ["dynamical"] },

    // 2008
    { y: 2008, type: "conf", t: "Video Registration Using Dynamic Textures", v: "ECCV", a: ["A. Ravichandran","R. Vidal"], url: "https://ieeexplore.ieee.org/abstract/document/5432206/", tags: ["dynamical"] },

    // 2007
    { y: 2007, type: "conf", t: "Mosaicing Nonrigid Dynamical Scenes", v: "Workshop Dynamic Vision", a: ["A. Ravichandran","R. Vidal"], url: "http://vision.jhu.edu/iccv2007-wdv/WDV07-ravichandran.pdf", tags: ["dynamical"] },

    // 2006
    { y: 2006, type: "conf", t: "Segmenting a Beating Heart using Polysegment and Spatial GPCA", v: "ISBI", a: ["A. Ravichandran","R. Vidal","H. Halperin"], url: "https://ieeexplore.ieee.org/abstract/document/1624996/", tags: ["detection","dynamical"] },

    // 2005
    { y: 2005, type: "conf", t: "Optical Flow Estimation & Segmentation of Multiple Moving Dynamic Textures", v: "CVPR", a: ["R. Vidal","A. Ravichandran"], url: "https://ieeexplore.ieee.org/abstract/document/1467485/", tags: ["dynamical"] }
  ],

  patents: [
    { y: 2025, t: "Class-incremental learning with pretrained machine learning models", num: "US 12406469 B2", url: "https://patents.google.com/patent/US12406469B2/en" },
    { y: 2024, t: "Feedback-based training for anomaly detection",                num: "US 12147878 B2", url: "https://patents.google.com/patent/US12147878B2/en" },
    { y: 2024, t: "Anomaly detection using feedback training",                    num: "US 11983243 B2", url: "https://patents.google.com/patent/US11983243B2/en" },
    { y: 2023, t: "Dynamically scaled training fleets for machine learning",      num: "US 11715033 B2", url: "https://patents.google.com/patent/US11715033B2/en" },
    { y: 2022, t: "Automated model selection for network-based image recognition",num: "US 11429813 B1", url: "https://patents.google.com/patent/US11429813B1/en" },
    { y: 2021, t: "Prototypical network algorithms for few-shot learning",        num: "US 10963754 B1", url: "https://patents.google.com/patent/US10963754B1/en" },
    { y: 2020, t: "Visual similarity and attribute manipulation using deep networks", num: "US 10824942 B1", url: "https://patents.google.com/patent/US10824942B1/en" },
    { y: 2020, t: "Parts-based visual similarity search",                         num: "US 10776417 B1", url: "https://patents.google.com/patent/US10776417B1/en" },
    { y: 2020, t: "Dynamically scaled training fleets for machine learning",      num: "US 10540608 B1", url: "https://patents.google.com/patent/US10540608B1/en" },
    { y: 2019, t: "Object recognition",                                           num: "US 10380461 B1", url: "https://patents.google.com/patent/US10380461B1/en" },
    { y: 2017, t: "Object recognition",                                           num: "US 9830534 B1",  url: "https://patents.google.com/patent/US9830534B1/en"  },
    { y: 2017, t: "Cluster-trained machine learning for image processing",        num: "US 9704054 B1",  url: "https://patents.google.com/patent/US9704054B1/en"  },
    { y: 2017, t: "Approaches for scene-based object tracking",                   num: "US 9697608 B1",  url: "https://patents.google.com/patent/US9697608B1/en"  },
    { y: 2015, t: "System and method for aligning video sequences",               num: "US 9025908 B2",  url: "https://patents.google.com/patent/US9025908B2/en"  },
    { y: 2015, t: "Recognizing three-dimensional objects",                        num: "US 9171195 B1",  url: "https://patents.google.com/patent/US9171195B1/en"  }
  ]
};
