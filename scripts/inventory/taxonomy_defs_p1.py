# -*- coding: utf-8 -*-
"""
taxonomy_defs_p1.py - Categories 1 to 18 Domain Definitions
"""

DEFS_P1 = {
    1: {
        "category_id": 1,
        "stable_id": "cat-01-curated-knowledge",
        "title": "Curated Knowledge, Developer Guides, Books & Awesome Collections",
        "short_title": "Curated Knowledge & Developer Guides",
        "slug": "01_curated_knowledge_developer_gu",
        "markdown_file": "categories/01_curated_knowledge_developer_gu.md",
        "meta_domain_id": "meta-meta-knowledge",
        "domain_boundaries": {
            "definition": "Curated knowledge aggregation, community-driven awesome lists, canonical developer roadmaps, interactive CS curricula, free programming books, and public API registries that synthesize technical literature and learning pathways.",
            "inclusions": [
                "Community-curated awesome lists and topic catalogs",
                "Interactive developer career roadmaps and skill trees",
                "Computer science interview prep and algorithmic curricula",
                "Free open-access programming books and reference texts",
                "Public and free API registries and developer sandboxes",
                "System architecture primers and software engineering cheat sheets"
            ],
            "exclusions": [
                {
                    "topic": "Framework-specific documentation and tutorials",
                    "redirect_category_id": 49,
                    "redirect_category_name": "Modern Frontend Frameworks, Reactive Web Engines (React/Vue/Svelte) & Bundlers",
                    "rationale": "Direct framework documentation belongs to the respective framework category."
                },
                {
                    "topic": "Standalone CLI developer tools",
                    "redirect_category_id": 46,
                    "redirect_category_name": "Developer Tooling, Shell Environments, Terminal Emulators & CLI Utilities",
                    "rationale": "Executable CLI utilities belong to developer tooling rather than curated reading lists."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 46,
                    "adjacent_category_name": "Developer Tooling, Shell Environments, Terminal Emulators & CLI Utilities",
                    "boundary_relation": "Provides curated catalogs of CLI utilities and terminal tools."
                },
                {
                    "adjacent_category_id": 34,
                    "adjacent_category_name": "EdTech, Adaptive Learning, Cognitive Scaffolding & STEM Assessment",
                    "boundary_relation": "Supplies syllabus references and pedagogical reading lists for adaptive learning platforms."
                }
            ]
        },
        "keywords": {
            "primary": ["awesome-list", "developer-roadmap", "computer-science-curriculum", "free-programming-books", "public-apis", "cheat-sheets", "study-plan", "interview-prep"],
            "secondary": ["algorithms-guide", "system-design-primer", "developer-handbook", "clean-code", "coding-interview", "api-directory", "learning-pathway"],
            "tools_and_frameworks": ["sindresorhus/awesome", "public-apis/public-apis", "EbookFoundation/free-programming-books", "kamranahmedse/developer-roadmap", "jwasham/coding-interview-university", "donnemartin/system-design-primer"],
            "architectural_patterns": ["Curated Markdown AST Linting", "Automated Link Health Validation CI", "Structured Taxonomy Indexing", "Community Contribution Governance"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-meta-knowledge",
            "parent_meta_domain_name": "Meta-Knowledge & Developer Resources",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-01-01",
                    "title": "Topic & Framework Awesome Catalogs",
                    "description": "Comprehensive, community-curated directories of open-source libraries, tools, and resources for specific domains.",
                    "focus_keywords": ["awesome-lists", "curated-resources", "topic-directories"]
                },
                {
                    "subdiscipline_id": "sub-01-02",
                    "title": "Interactive Developer Roadmaps & Careers",
                    "description": "Step-by-step career path guides, technical skill progressions, and role-based milestone charts for software engineers.",
                    "focus_keywords": ["developer-roadmaps", "skill-trees", "career-pathways"]
                },
                {
                    "subdiscipline_id": "sub-01-03",
                    "title": "Computer Science Foundations & Systems Design",
                    "description": "Rigorous CS university curricula, distributed systems design primers, and algorithmic interview preparation syllabi.",
                    "focus_keywords": ["computer-science-curricula", "systems-design", "interview-preparation"]
                },
                {
                    "subdiscipline_id": "sub-01-04",
                    "title": "Open Source Books & Canonical Technical Literature",
                    "description": "Free, open-access technical books, language specifications, and software engineering philosophy manuals.",
                    "focus_keywords": ["free-programming-books", "open-textbooks", "technical-reading-lists"]
                },
                {
                    "subdiscipline_id": "sub-01-05",
                    "title": "Public APIs & Open Data Registries",
                    "description": "Centralized catalogs of public HTTP REST/GraphQL APIs, endpoints, authentication tiers, and developer sandboxes.",
                    "focus_keywords": ["public-apis", "open-data-catalogs", "free-tier-endpoints"]
                }
            ],
            "adjacent_categories": [34, 46, 53, 55]
        },
        "cross_category_tags": ["tag-developer-productivity"]
    },
    2: {
        "category_id": 2,
        "stable_id": "cat-02-ai-foundation-models",
        "title": "Artificial Intelligence, Large Language Models, Foundation Models & Quantization",
        "short_title": "Foundation Models, LLMs & Quantization",
        "slug": "02_artificial_intelligence_large_.md",
        "markdown_file": "categories/02_artificial_intelligence_large_.md",
        "meta_domain_id": "meta-artificial-intelligence",
        "domain_boundaries": {
            "definition": "Pre-trained foundation models, Large Language Models (LLMs), Transformer architectures, efficient model serving engines, quantization techniques (GGUF, AWQ, GPTQ), and parameter-efficient fine-tuning (LoRA, QLoRA).",
            "inclusions": [
                "Transformer model architectures and pre-trained foundation weights",
                "High-throughput LLM inference engines (vLLM, Ollama, llama.cpp, TGI)",
                "Model quantization algorithms and formats (GGUF, AWQ, GPTQ, EXL2)",
                "Parameter-efficient fine-tuning frameworks (PEFT, LoRA, QLoRA, Unsloth)",
                "FlashAttention, PagedAttention, and KV cache optimization runtimes",
                "Alignment and reinforcement learning from human/AI feedback (RLHF, DPO, PPO)"
            ],
            "exclusions": [
                {
                    "topic": "Multi-agent orchestration and swarms",
                    "redirect_category_id": 3,
                    "redirect_category_name": "Multi-Agent Systems, Autonomous Swarms, AI Orchestration & MCP Tools",
                    "rationale": "Multi-agent coordination, agent memory, and MCP tools belong to category 03."
                },
                {
                    "topic": "Computer vision and image diffusion",
                    "redirect_category_id": 4,
                    "redirect_category_name": "Computer Vision, Multimodal AI, Diffusion & Neural Rendering (NeRF/3D-GS)",
                    "rationale": "Image generation and visual perception models belong to category 04."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 3,
                    "adjacent_category_name": "Multi-Agent Systems, Autonomous Swarms, AI Orchestration & MCP Tools",
                    "boundary_relation": "Provides foundation model inference backends to multi-agent planners and swarms."
                },
                {
                    "adjacent_category_id": 37,
                    "adjacent_category_name": "Database Engines, Distributed SQL, NoSQL, Vector DBs & Persistent Caches",
                    "boundary_relation": "Integrates with vector databases for Retrieval-Augmented Generation (RAG) context retrieval."
                }
            ]
        },
        "keywords": {
            "primary": ["llm", "transformers", "foundation-models", "quantization", "gguf", "vllm", "ollama", "llama-cpp", "lora", "fine-tuning"],
            "secondary": ["pagedattention", "flashattention", "awq", "gptq", "dpo", "rlhf", "huggingface", "context-window", "kv-cache", "unsloth"],
            "tools_and_frameworks": ["huggingface/transformers", "ggerganov/llama.cpp", "vllm-project/vllm", "ollama/ollama", "unslothai/unsloth", "tgi"],
            "architectural_patterns": ["KV Cache Paged Memory Allocation", "Continuous Batching Inference", "Quantized Matrix Multiplication (W4A16)", "Parameter-Efficient Adapter Merging"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-artificial-intelligence",
            "parent_meta_domain_name": "Artificial Intelligence & Cognitive Computing",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-02-01",
                    "title": "Foundation Model Architectures & Pre-training",
                    "description": "Dense and Mixture-of-Experts (MoE) transformer architectures, tokenization, positional embeddings, and training pipelines.",
                    "focus_keywords": ["transformers", "mixture-of-experts", "rope-embeddings", "pre-training"]
                },
                {
                    "subdiscipline_id": "sub-02-02",
                    "title": "High-Throughput Local Inference Runtimes",
                    "description": "Optimized execution runtimes enabling low-latency, high-concurrency local LLM serving on CPU and GPU hardware.",
                    "focus_keywords": ["vllm", "llama.cpp", "ollama", "continuous-batching"]
                },
                {
                    "subdiscipline_id": "sub-02-03",
                    "title": "Model Quantization & Weight Compression",
                    "description": "Techniques reducing model precision to 4-bit and 8-bit representations while preserving perplexity and reasoning capability.",
                    "focus_keywords": ["gguf", "awq", "gptq", "exl2", "weight-quantization"]
                },
                {
                    "subdiscipline_id": "sub-02-04",
                    "title": "Parameter-Efficient Fine-Tuning & Alignment",
                    "description": "Methods for adapting foundation models with minimal compute overhead using rank decomposition and preference optimization.",
                    "focus_keywords": ["lora", "qlora", "peft", "dpo", "rlhf"]
                }
            ],
            "adjacent_categories": [3, 4, 5, 37, 55]
        },
        "cross_category_tags": ["tag-machine-learning", "tag-high-performance-computing"]
    },
    3: {
        "category_id": 3,
        "stable_id": "cat-03-multi-agent-systems",
        "title": "Multi-Agent Systems, Autonomous Swarms, AI Orchestration & MCP Tools",
        "short_title": "Multi-Agent Systems & AI Orchestration",
        "slug": "03_multi_agent_systems_autonomous.md",
        "markdown_file": "categories/03_multi_agent_systems_autonomous.md",
        "meta_domain_id": "meta-artificial-intelligence",
        "domain_boundaries": {
            "definition": "Autonomous multi-agent coordination frameworks, cognitive architectures, swarm intelligence, Model Context Protocol (MCP) tool integrations, planning engines, execution DAGs, and autonomous developer agents.",
            "inclusions": [
                "Multi-agent coordination frameworks (CrewAI, AutoGen, LangGraph, MetaGPT)",
                "Model Context Protocol (MCP) servers, clients, and tool specifications",
                "Autonomous coding, research, and general task execution agents",
                "Cognitive memory, reflective loops, and scratchpad architectures",
                "Directed acyclic graph (DAG) workflow orchestrators for LLMs",
                "Swarm intelligence, role specialization, and consensus voting protocols"
            ],
            "exclusions": [
                {
                    "topic": "Core transformer model training and quantization",
                    "redirect_category_id": 2,
                    "redirect_category_name": "Artificial Intelligence, Large Language Models, Foundation Models & Quantization",
                    "rationale": "Model weights and raw token generation runtimes belong to category 02."
                },
                {
                    "topic": "Physical humanoid robot kinematics",
                    "redirect_category_id": 6,
                    "redirect_category_name": "Robotics, Humanoid Kinematics, Dynamics, Actuators & Physics Simulation",
                    "rationale": "Embodied physical robots belong to robotics category 06."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 2,
                    "adjacent_category_name": "Artificial Intelligence, Large Language Models, Foundation Models & Quantization",
                    "boundary_relation": "Consumes model inference APIs from foundation model runtimes."
                },
                {
                    "adjacent_category_id": 40,
                    "adjacent_category_name": "CI/CD Automation, GitOps & Infrastructure-as-Code (Terraform/Ansible)",
                    "boundary_relation": "Triggers automated build and deployment pipelines from autonomous agent workflows."
                }
            ]
        },
        "keywords": {
            "primary": ["multi-agent", "autonomous-agents", "mcp", "langchain", "crewai", "autogen", "langgraph", "agentic-ai", "tool-use", "swarm-intelligence"],
            "secondary": ["cognitive-architecture", "dag-planning", "agent-memory", "reflection", "metagpt", "chatdev", "react-prompting", "mcp-server"],
            "tools_and_frameworks": ["langchain-ai/langchain", "crewAIInc/crewAI", "microsoft/autogen", "anthropics/model-context-protocol", "geekan/MetaGPT", "langgraph"],
            "architectural_patterns": ["ReAct (Reason + Act) Feedback Loop", "Dynamic Execution DAG Scheduling", "Model Context Protocol Tool Dispatch", "Hierarchical Agent Supervision"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-artificial-intelligence",
            "parent_meta_domain_name": "Artificial Intelligence & Cognitive Computing",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-03-01",
                    "title": "Multi-Agent Coordination & Swarm Protocols",
                    "description": "Architectures enabling multiple specialized AI personas to collaborate, debate, and verify outputs.",
                    "focus_keywords": ["multi-agent-orchestration", "crewai", "autogen", "swarm-consensus"]
                },
                {
                    "subdiscipline_id": "sub-03-02",
                    "title": "Model Context Protocol (MCP) & Tool Systems",
                    "description": "Standardized protocol implementations enabling agents to query local and remote tools, resources, and databases.",
                    "focus_keywords": ["mcp-server", "mcp-client", "tool-dispatch", "context-injection"]
                },
                {
                    "subdiscipline_id": "sub-03-03",
                    "title": "Autonomous Software Engineering & Coding Agents",
                    "description": "Self-healing, code-writing agents capable of inspecting repositories, editing files, running tests, and opening PRs.",
                    "focus_keywords": ["autonomous-coding", "metagpt", "swe-bench", "self-healing-code"]
                },
                {
                    "subdiscipline_id": "sub-03-04",
                    "title": "Cognitive Memory & Stateful Graph Workflows",
                    "description": "Graph-based execution engines managing persistent short- and long-term memory, state checkpoints, and human-in-the-loop gates.",
                    "focus_keywords": ["langgraph", "stateful-graphs", "agent-memory", "human-in-the-loop"]
                }
            ],
            "adjacent_categories": [2, 4, 38, 40, 53]
        },
        "cross_category_tags": ["tag-machine-learning", "tag-distributed-systems"]
    },
    4: {
        "category_id": 4,
        "stable_id": "cat-04-computer-vision-multimodal",
        "title": "Computer Vision, Multimodal AI, Diffusion & Neural Rendering (NeRF/3D-GS)",
        "short_title": "Computer Vision & Multimodal AI",
        "slug": "04_computer_vision_multimodal_ai_.md",
        "markdown_file": "categories/04_computer_vision_multimodal_ai_.md",
        "meta_domain_id": "meta-artificial-intelligence",
        "domain_boundaries": {
            "definition": "Visual perception, image segmentation, object detection, multimodal vision-language models (VLM), generative latent diffusion pipelines, and 3D neural rendering including Neural Radiance Fields (NeRF) and 3D Gaussian Splatting (3D-GS).",
            "inclusions": [
                "Generative latent diffusion models (Stable Diffusion, Flux, ComfyUI, ControlNet)",
                "Real-time object detection and instance segmentation (YOLO, Segment Anything, SAM)",
                "3D neural scene representations (NeRF, 3D Gaussian Splatting, instant-ngp)",
                "Multimodal Vision-Language Models (CLIP, BLIP, LLaVA, CogVLM)",
                "OpenCV computer vision filters, optical flow, and edge detection",
                "Video generation, frame interpolation, and motion transfer models"
            ],
            "exclusions": [
                {
                    "topic": "Video codecs and streaming infrastructure",
                    "redirect_category_id": 54,
                    "redirect_category_name": "Multimedia Processing, Audio/Video Codecs, FFmpeg & Streaming Pipelines",
                    "rationale": "FFmpeg transcoding, WebRTC, and HLS streaming belong to multimedia processing category 54."
                },
                {
                    "topic": "Traditional game engine graphics APIs",
                    "redirect_category_id": 48,
                    "redirect_category_name": "Game Development Engines, 2D/3D Graphics APIs & Shaders (WebGL/Vulkan)",
                    "rationale": "Vulkan, WebGL, and real-time game shaders belong to category 48."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 2,
                    "adjacent_category_name": "Artificial Intelligence, Large Language Models, Foundation Models & Quantization",
                    "boundary_relation": "Supplies visual embeddings and cross-attention adapters for multimodal LLMs."
                },
                {
                    "adjacent_category_id": 7,
                    "adjacent_category_name": "Autonomous Vehicles, Mobile Robotics, LiDAR SLAM & Drone Flight Control",
                    "boundary_relation": "Provides visual perception and object detection feeds for vehicle obstacle avoidance."
                }
            ]
        },
        "keywords": {
            "primary": ["computer-vision", "diffusion-models", "stable-diffusion", "comfyui", "yolo", "segment-anything", "gaussian-splatting", "nerf", "multimodal", "clip"],
            "secondary": ["object-detection", "image-segmentation", "controlnet", "llava", "flux", "latent-diffusion", "vlm", "optical-flow", "neural-rendering"],
            "tools_and_frameworks": ["comfyanonymous/ComfyUI", "ultralytics/yolov5", "facebookresearch/segment-anything", "CompVis/stable-diffusion", "nerfstudio-project/nerfstudio", "openai/CLIP"],
            "architectural_patterns": ["Denoising Diffusion Probabilistic Model (DDPM)", "Feature Pyramid Network (FPN)", "Cross-Attention Multimodal Fusion", "Differentiable 3D Gaussian Rasterization"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-artificial-intelligence",
            "parent_meta_domain_name": "Artificial Intelligence & Cognitive Computing",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-04-01",
                    "title": "Generative Latent Diffusion & Image Synthesis",
                    "description": "Text-to-image and image-to-image generation frameworks utilizing latent diffusion and flow matching.",
                    "focus_keywords": ["stable-diffusion", "comfyui", "flux", "controlnet", "latent-diffusion"]
                },
                {
                    "subdiscipline_id": "sub-04-02",
                    "title": "Object Detection & Spatial Segmentation",
                    "description": "High-speed convolutional and vision transformer models identifying bounding boxes and zero-shot segmentation masks.",
                    "focus_keywords": ["yolo", "segment-anything", "instance-segmentation", "panoptic-segmentation"]
                },
                {
                    "subdiscipline_id": "sub-04-03",
                    "title": "3D Neural Radiance Fields & Gaussian Splatting",
                    "description": "Volumetric and explicit point-cloud neural rendering reconstructing photorealistic 3D environments from 2D photos.",
                    "focus_keywords": ["nerf", "3d-gaussian-splatting", "neural-radiance-fields", "instant-ngp"]
                },
                {
                    "subdiscipline_id": "sub-04-04",
                    "title": "Multimodal Vision-Language Models (VLMs)",
                    "description": "Joint vision-language representations enabling complex visual reasoning, document understanding, and image captioning.",
                    "focus_keywords": ["vlm", "clip", "llava", "visual-question-answering"]
                }
            ],
            "adjacent_categories": [2, 6, 7, 48, 54]
        },
        "cross_category_tags": ["tag-machine-learning", "tag-computer-vision-graphics"]
    },
    5: {
        "category_id": 5,
        "stable_id": "cat-05-speech-voice-audio",
        "title": "Speech, Voice AI, Audio Processing, Audio Synthesis & Music Generation",
        "short_title": "Speech, Voice AI & Audio Processing",
        "slug": "05_speech_voice_ai_audio_processi.md",
        "markdown_file": "categories/05_speech_voice_ai_audio_processi.md",
        "meta_domain_id": "meta-artificial-intelligence",
        "domain_boundaries": {
            "definition": "Automatic Speech Recognition (ASR), Text-to-Speech (TTS), neural voice cloning, acoustic feature extraction, real-time voice conversion, and deep generative audio/music synthesis.",
            "inclusions": [
                "Automatic speech recognition (Whisper, faster-whisper, WhisperX)",
                "Neural text-to-speech engines (Piper, Bark, CosyVoice, ChatTTS)",
                "Zero-shot voice cloning and speaker embedding extraction",
                "Neural audio separation, speech denoising, and echo cancellation",
                "Generative music composition and sound effect models",
                "Neural audio codecs and discrete tokenizers (EnCodec, DAC)"
            ],
            "exclusions": [
                {
                    "topic": "Video codecs and streaming protocols",
                    "redirect_category_id": 54,
                    "redirect_category_name": "Multimedia Processing, Audio/Video Codecs, FFmpeg & Streaming Pipelines",
                    "rationale": "Video streaming pipelines and generic container codecs belong to multimedia processing 54."
                },
                {
                    "topic": "Physical acoustic levitation and transducers",
                    "redirect_category_id": 23,
                    "redirect_category_name": "Acoustic Levitation, Acoustofluidics & Phased Array Manipulation",
                    "rationale": "Physical acoustic force fields and levitation belong to category 23."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 3,
                    "adjacent_category_name": "Multi-Agent Systems, Autonomous Swarms, AI Orchestration & MCP Tools",
                    "boundary_relation": "Provides voice I/O channels and streaming speech interfaces for autonomous conversational agents."
                },
                {
                    "adjacent_category_id": 54,
                    "adjacent_category_name": "Multimedia Processing, Audio/Video Codecs, FFmpeg & Streaming Pipelines",
                    "boundary_relation": "Sends processed audio streams into multimedia muxers and broadcasting servers."
                }
            ]
        },
        "keywords": {
            "primary": ["speech-recognition", "tts", "whisper", "voice-cloning", "audio-processing", "speech-synthesis", "neural-audio", "asr", "music-generation", "voice-ai"],
            "secondary": ["faster-whisper", "piper-tts", "bark", "cosyvoice", "encodec", "audio-separation", "vocoder", "mel-spectrogram", "speaker-diarization"],
            "tools_and_frameworks": ["openai/whisper", "rhasspy/piper", "suno-ai/bark", "SYSTRAN/faster-whisper", "FunAudioLLM/CosyVoice", "m-bain/whisperX"],
            "architectural_patterns": ["Sequence-to-Sequence Attention Transduction", "Neural Vocoding (HiFi-GAN)", "Discrete Audio Residual Vector Quantization", "CTC Loss Beam Search"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-artificial-intelligence",
            "parent_meta_domain_name": "Artificial Intelligence & Cognitive Computing",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-05-01",
                    "title": "Automatic Speech Recognition & Diarization",
                    "description": "Robust acoustic transcription of spoken multi-lingual audio into text with word-level timestamps and speaker identification.",
                    "focus_keywords": ["whisper", "asr", "speech-to-text", "speaker-diarization"]
                },
                {
                    "subdiscipline_id": "sub-05-02",
                    "title": "Neural Text-to-Speech & Voice Cloning",
                    "description": "High-fidelity expressive speech synthesis with zero-shot timbre transfer from reference voice clips.",
                    "focus_keywords": ["tts", "voice-cloning", "piper", "cosyvoice", "neural-vocoder"]
                },
                {
                    "subdiscipline_id": "sub-05-03",
                    "title": "Audio Enhancement & Source Separation",
                    "description": "Deep learning models isolating vocals, instruments, and speech from noisy background environments.",
                    "focus_keywords": ["audio-separation", "denoising", "demucs", "speech-enhancement"]
                },
                {
                    "subdiscipline_id": "sub-05-04",
                    "title": "Generative Music & Environmental Sound Synthesis",
                    "description": "Models creating coherent musical pieces, harmonies, and Foley sound effects conditioned on text prompts.",
                    "focus_keywords": ["music-generation", "sound-effects", "audiocraft", "generative-music"]
                }
            ],
            "adjacent_categories": [2, 3, 23, 54]
        },
        "cross_category_tags": ["tag-machine-learning", "tag-audio-and-speech"]
    },
    6: {
        "category_id": 6,
        "stable_id": "cat-06-robotics-kinematics",
        "title": "Robotics, Humanoid Kinematics, Dynamics, Actuators & Physics Simulation",
        "short_title": "Robotics, Humanoid Kinematics & Simulation",
        "slug": "06_robotics_humanoid_kinematics_d.md",
        "markdown_file": "categories/06_robotics_humanoid_kinematics_d.md",
        "meta_domain_id": "meta-autonomous-robotics",
        "domain_boundaries": {
            "definition": "Rigid-body kinematics and dynamics algorithms, humanoid bipedal locomotion, zero-moment point (ZMP) balance, robotic actuator control, spatial trajectory optimization, and GPU-accelerated physics simulation.",
            "inclusions": [
                "Forward and inverse kinematics engines (Pinocchio, KDL)",
                "Rigid body physics simulators (MuJoCo, Isaac Gym, Bullet Physics, Drake)",
                "Humanoid bipedal and quadrupedal locomotion controllers",
                "Robotic trajectory optimization and collision-free motion planning (MoveIt)",
                "Direct-drive and quasi-direct-drive actuator torque controllers",
                "Robot Operating System (ROS/ROS2) core robotic communication stacks"
            ],
            "exclusions": [
                {
                    "topic": "Autonomous vehicle road driving and traffic navigation",
                    "redirect_category_id": 7,
                    "redirect_category_name": "Autonomous Vehicles, Mobile Robotics, LiDAR SLAM & Drone Flight Control",
                    "rationale": "Automotive driving stacks and street LiDAR SLAM belong to category 07."
                },
                {
                    "topic": "Industrial PLC ladder logic automation",
                    "redirect_category_id": 31,
                    "redirect_category_name": "Industrial Automation, SCADA, PLC Ladder Logic, OPC-UA & Hardware Security",
                    "rationale": "Fixed factory floor automation and PLC ladder logic belong to category 31."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 7,
                    "adjacent_category_name": "Autonomous Vehicles, Mobile Robotics, LiDAR SLAM & Drone Flight Control",
                    "boundary_relation": "Shares ROS2 message buses and spatial coordinate transformation frames."
                },
                {
                    "adjacent_category_id": 4,
                    "adjacent_category_name": "Computer Vision, Multimodal AI, Diffusion & Neural Rendering (NeRF/3D-GS)",
                    "boundary_relation": "Consumes 3D perception feeds for object grasping and robotic manipulation."
                }
            ]
        },
        "keywords": {
            "primary": ["robotics", "humanoid", "kinematics", "dynamics", "mujoco", "ros2", "motion-planning", "pinocchio", "actuators", "physics-simulation"],
            "secondary": ["isaac-gym", "bullet-physics", "drake", "moveit", "bipedal-locomotion", "quadruped", "zmp-balance", "urdf", "inverse-kinematics"],
            "tools_and_frameworks": ["google-deepmind/mujoco", "stack-of-tasks/pinocchio", "ros-planning/moveit2", "bulletphysics/bullet3", "RobotLocomotion/drake"],
            "architectural_patterns": ["Recursive Newton-Euler Dynamic Algorithm (RNEA)", "Articulated Body Algorithm (ABA)", "Zero-Moment Point Balance Stabilization", "Whole-Body Model Predictive Control (MPC)"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-autonomous-robotics",
            "parent_meta_domain_name": "Robotics, Autonomous Vehicles & Mobility",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-06-01",
                    "title": "Rigid Body Kinematics & Spatial Dynamics",
                    "description": "Algorithms computing link positions, Jacobians, and operational space inertias for high-degree-of-freedom mechanisms.",
                    "focus_keywords": ["pinocchio", "inverse-kinematics", "spatial-dynamics", "jacobians"]
                },
                {
                    "subdiscipline_id": "sub-06-02",
                    "title": "Physics Simulation & Sim-to-Real Transfer",
                    "description": "Contact dynamics, friction cones, and GPU-parallelized environment simulation for reinforcement learning.",
                    "focus_keywords": ["mujoco", "isaac-gym", "sim-to-real", "contact-dynamics"]
                },
                {
                    "subdiscipline_id": "sub-06-03",
                    "title": "Humanoid & Legged Locomotion Control",
                    "description": "Capture point dynamics, gait scheduling, and balance recovery algorithms for bipedal and quadrupedal robots.",
                    "focus_keywords": ["humanoid-locomotion", "quadruped-gait", "zmp", "capture-point"]
                },
                {
                    "subdiscipline_id": "sub-06-04",
                    "title": "Robotic Manipulation & Motion Planning",
                    "description": "Collision-free end-effector path planning, trajectory generation, and multi-finger robotic grasping.",
                    "focus_keywords": ["moveit", "robotic-manipulation", "trajectory-optimization", "grasping"]
                }
            ],
            "adjacent_categories": [4, 7, 8, 31]
        },
        "cross_category_tags": ["tag-machine-learning", "tag-embedded-and-iot"]
    },
    7: {
        "category_id": 7,
        "stable_id": "cat-07-autonomous-vehicles-slam",
        "title": "Autonomous Vehicles, Mobile Robotics, LiDAR SLAM & Drone Flight Control",
        "short_title": "Autonomous Vehicles & LiDAR SLAM",
        "slug": "07_autonomous_vehicles_mobile_rob.md",
        "markdown_file": "categories/07_autonomous_vehicles_mobile_rob.md",
        "meta_domain_id": "meta-autonomous-robotics",
        "domain_boundaries": {
            "definition": "Autonomous driving software stacks, mobile robotic navigation, simultaneous localization and mapping (SLAM) using LiDAR and visual-inertial odometry, and UAV/drone autopilot systems.",
            "inclusions": [
                "Full autonomous driving software architectures (Autoware, Apollo)",
                "2D and 3D LiDAR SLAM systems (Cartographer, Fast-LIO, LIO-SAM, LOAM)",
                "Open-source drone and UAV flight controllers (PX4, ArduPilot)",
                "Mobile robot path planning algorithms (A*, Hybrid A*, TEB local planner)",
                "Multi-sensor fusion (Extended Kalman Filters, factor graph optimization)",
                "High-definition (HD) mapping, point cloud registration, and lane tracking"
            ],
            "exclusions": [
                {
                    "topic": "Spacecraft orbital astrodynamics and planetary entry",
                    "redirect_category_id": 14,
                    "redirect_category_name": "Space Systems, Orbital Astrodynamics, Satellite Tracking & Rocket Propulsion",
                    "rationale": "Spacecraft orbital mechanics belong to space systems category 14."
                },
                {
                    "topic": "Marine surface ship hydrodynamics and sonar",
                    "redirect_category_id": 24,
                    "redirect_category_name": "Marine Hydrodynamics, Sonar Transducer Arrays & Ocean Engineering",
                    "rationale": "Marine watercraft seakeeping belongs to category 24."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 6,
                    "adjacent_category_name": "Robotics, Humanoid Kinematics, Dynamics, Actuators & Physics Simulation",
                    "boundary_relation": "Shares low-level motor drive commands and chassis kinematics models."
                },
                {
                    "adjacent_category_id": 29,
                    "adjacent_category_name": "Smart Cities, Building Information Modeling (BIM/IFC) & Urban Mobility",
                    "boundary_relation": "Feeds real-time vehicle telemetry into urban traffic microsimulators."
                }
            ]
        },
        "keywords": {
            "primary": ["autonomous-vehicles", "slam", "lidar", "autoware", "px4", "ardupilot", "cartographer", "sensor-fusion", "path-planning", "drone-control"],
            "secondary": ["fast-lio", "lio-sam", "kalman-filter", "hybrid-a-star", "odometry", "point-cloud-mapping", "hd-map", "visual-inertial", "teb-planner"],
            "tools_and_frameworks": ["autowarefoundation/autoware", "PX4/PX4-Autopilot", "ArduPilot/ardupilot", "cartographer-project/cartographer", "hku-mars/FAST_LIO"],
            "architectural_patterns": ["Factor Graph Non-Linear Least Squares Optimization", "Extended Kalman Filter State Estimation", "Hierarchical Lattice Motion Planning", "Hierarchical Finite State Machine Failsafe"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-autonomous-robotics",
            "parent_meta_domain_name": "Robotics, Autonomous Vehicles & Mobility",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-07-01",
                    "title": "Autonomous Driving Software Stacks",
                    "description": "Full-scale perception, planning, control, and localization stacks designed for level 4 road autonomy.",
                    "focus_keywords": ["autoware", "apollo", "autonomous-driving", "lane-detection"]
                },
                {
                    "subdiscipline_id": "sub-07-02",
                    "title": "LiDAR & Visual-Inertial SLAM",
                    "description": "Real-time state estimation and metric dense map building using scanning laser ranges and inertial measurement units.",
                    "focus_keywords": ["fast-lio", "cartographer", "lidar-slam", "state-estimation"]
                },
                {
                    "subdiscipline_id": "sub-07-03",
                    "title": "Drone & UAV Autopilot Systems",
                    "description": "Real-time embedded flight control software for multi-rotors, fixed-wing aircraft, and VTOL drones.",
                    "focus_keywords": ["px4", "ardupilot", "flight-controller", "vtol-control"]
                },
                {
                    "subdiscipline_id": "sub-07-04",
                    "title": "Mobile Robot Path Planning & Obstacle Avoidance",
                    "description": "Global topological routing and local obstacle avoidance algorithms for AGVs and mobile warehouse robots.",
                    "focus_keywords": ["hybrid-a-star", "teb-local-planner", "dynamic-window-approach", "obstacle-avoidance"]
                }
            ],
            "adjacent_categories": [4, 6, 21, 29, 31]
        },
        "cross_category_tags": ["tag-autonomous-mobility", "tag-embedded-and-iot"]
    },
    8: {
        "category_id": 8,
        "stable_id": "cat-08-semiconductor-eda-riscv",
        "title": "Semiconductor, Silicon EDA, RTL-to-GDSII, FPGA & RISC-V Architecture",
        "short_title": "Semiconductor, Silicon EDA & RISC-V",
        "slug": "08_semiconductor_silicon_eda_rtl_.md",
        "markdown_file": "categories/08_semiconductor_silicon_eda_rtl_.md",
        "meta_domain_id": "meta-hardware-quantum-physics",
        "domain_boundaries": {
            "definition": "Electronic Design Automation (EDA), register-transfer level (RTL) synthesis, physical placement and routing (P&R), formal hardware verification, FPGA bitstream toolchains, and open-source RISC-V processor architectures.",
            "inclusions": [
                "Open-source ASIC RTL-to-GDSII toolchains (OpenLane, OpenROAD, Magic, Netgen)",
                "RTL logic synthesis and optimization engines (Yosys)",
                "High-performance hardware simulation and linting (Verilator, Icarus Verilog)",
                "Open-source RISC-V cores, SoC generators, and instruction set extensions",
                "FPGA bitstream compilation toolchains (Project IceStorm, NextPNR)",
                "Modern Hardware Description Languages (Chisel, SpinalHDL, Amaranth)"
            ],
            "exclusions": [
                {
                    "topic": "Microcontroller firmware and embedded C code",
                    "redirect_category_id": 45,
                    "redirect_category_name": "Systems Programming, Low-Level Runtimes, Memory Safety & WebAssembly (Wasm)",
                    "rationale": "Embedded C/Rust application code belongs to systems programming category 45."
                },
                {
                    "topic": "Quantum logic gates and superconducting qubits",
                    "redirect_category_id": 9,
                    "redirect_category_name": "Quantum Computing, Quantum Algorithms, Circuit Simulation & Error Correction",
                    "rationale": "Quantum circuit simulation and qubits belong to category 09."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 43,
                    "adjacent_category_name": "Operating Systems, Linux Kernels, Low-Level Drivers & Emulators",
                    "boundary_relation": "Provides cycle-accurate instruction set models for hardware emulator targets."
                },
                {
                    "adjacent_category_id": 33,
                    "adjacent_category_name": "Formal Verification, Theorem Proving & Mathematical Proof Systems",
                    "boundary_relation": "Applies formal model checking to prove absence of hardware deadlocks in RTL designs."
                }
            ]
        },
        "keywords": {
            "primary": ["eda", "semiconductor", "riscv", "verilog", "vhdl", "yosys", "openlane", "verilator", "fpga", "silicon-design", "asic"],
            "secondary": ["openroad", "nextpnr", "chisel", "spinalhdl", "gdsii", "logic-synthesis", "place-and-route", "systemverilog", "timing-analysis"],
            "tools_and_frameworks": ["YosysHQ/yosys", "The-OpenROAD-Project/OpenLane", "verilator/verilator", "chipsalliance/chisel", "YosysHQ/nextpnr"],
            "architectural_patterns": ["Static Timing Analysis (STA)", "Logic Equivalence Checking", "Multi-Stage Pipelining RTL", "Decoupled Crossbar Interconnect (AXI/TileLink)"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-hardware-quantum-physics",
            "parent_meta_domain_name": "Semiconductors, Quantum Systems & Applied Physics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-08-01",
                    "title": "RTL Synthesis & Logic Optimization",
                    "description": "Translating behavioral Verilog/VHDL descriptions into optimized technology-mapped gate-level netlists.",
                    "focus_keywords": ["yosys", "logic-synthesis", "gate-level-netlist", "technology-mapping"]
                },
                {
                    "subdiscipline_id": "sub-08-02",
                    "title": "Physical Design & RTL-to-GDSII Toolchains",
                    "description": "Floorplanning, placement, clock tree synthesis, and routing yielding manufacturing-ready GDSII/OASIS masks.",
                    "focus_keywords": ["openlane", "openroad", "floorplanning", "gdsii-generation"]
                },
                {
                    "subdiscipline_id": "sub-08-03",
                    "title": "Cycle-Accurate Hardware Simulation & Emulation",
                    "description": "High-throughput simulation converting SystemVerilog into high-speed C++ multithreaded simulation models.",
                    "focus_keywords": ["verilator", "cycle-accurate-simulation", "testbenches", "hardware-linting"]
                },
                {
                    "subdiscipline_id": "sub-08-04",
                    "title": "Open RISC-V Processor Cores & SoCs",
                    "description": "Scalable open-source CPU architectures, superscalar out-of-order pipelines, and vector extensions.",
                    "focus_keywords": ["riscv", "cpu-core", "tilelink", "axi-bus", "rv64gc"]
                }
            ],
            "adjacent_categories": [9, 31, 33, 43, 45]
        },
        "cross_category_tags": ["tag-systems-programming", "tag-high-performance-computing", "tag-formal-methods-verification"]
    },
    9: {
        "category_id": 9,
        "stable_id": "cat-09-quantum-computing-algorithms",
        "title": "Quantum Computing, Quantum Algorithms, Circuit Simulation & Error Correction",
        "short_title": "Quantum Computing & Circuit Simulation",
        "slug": "09_quantum_computing_quantum_algo.md",
        "markdown_file": "categories/09_quantum_computing_quantum_algo.md",
        "meta_domain_id": "meta-hardware-quantum-physics",
        "domain_boundaries": {
            "definition": "Quantum circuit synthesis, unitary statevector and density matrix simulation, quantum variational algorithms (VQE, QAOA), quantum error correction (QEC surface codes), and quantum programming frameworks.",
            "inclusions": [
                "Open-source quantum computing SDKs (Qiskit, Cirq, PennyLane, Braket)",
                "High-performance statevector and tensor network quantum simulators",
                "Variational Quantum Eigensolvers (VQE) and Quantum Approximate Optimization (QAOA)",
                "Quantum Error Correction (QEC) syndromes and Surface Code lattice decoders",
                "Quantum circuit transpilation, gate decomposition, and Solovay-Kitaev compilation",
                "Quantum chemistry and Hamiltonian ground-state energy calculations"
            ],
            "exclusions": [
                {
                    "topic": "Post-quantum classical cryptographic primitives",
                    "redirect_category_id": 32,
                    "redirect_category_name": "Cryptography, Zero-Knowledge Proofs (ZKP), Post-Quantum & Privacy Tech",
                    "rationale": "Lattice-based classical algorithms (Kyber/Dilithium) belong to cryptography category 32."
                },
                {
                    "topic": "Solid-state cryogenic refrigeration hardware",
                    "redirect_category_id": 10,
                    "redirect_category_name": "Superconducting Systems, Cryogenics & Energy Storage (SMES)",
                    "rationale": "Physical dilution refrigerators and superconducting material modeling belong to category 10."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 10,
                    "adjacent_category_name": "Superconducting Systems, Cryogenics & Energy Storage (SMES)",
                    "boundary_relation": "Maps ideal quantum gates to microwave pulses operating inside dilution cryostats."
                },
                {
                    "adjacent_category_id": 32,
                    "adjacent_category_name": "Cryptography, Zero-Knowledge Proofs (ZKP), Post-Quantum & Privacy Tech",
                    "boundary_relation": "Assesses vulnerability of asymmetric public-key cryptosystems against Shor's algorithm."
                }
            ]
        },
        "keywords": {
            "primary": ["quantum-computing", "qiskit", "cirq", "pennylane", "quantum-circuits", "qaoa", "vqe", "quantum-algorithms", "qubit", "error-correction"],
            "secondary": ["statevector", "surface-code", "tensor-network", "quantum-supremacy", "unitary-gates", "hamiltonian", "openqasm", "bloch-sphere"],
            "tools_and_frameworks": ["Qiskit/qiskit", "quantumlib/Cirq", "PennyLaneAI/pennylane", "Qiskit/qiskit-aer", "amazon-braket/amazon-braket-sdk-python"],
            "architectural_patterns": ["Unitary Statevector Tensor Product Expansion", "Syndrome Extraction MWPM Decoding", "Variational Quantum-Classical Optimization Loop", "Solovay-Kitaev Gate Transpilation"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-hardware-quantum-physics",
            "parent_meta_domain_name": "Semiconductors, Quantum Systems & Applied Physics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-09-01",
                    "title": "Quantum Circuit Compilation & Simulation",
                    "description": "High-fidelity simulation of n-qubit registers using complex128 statevector and matrix-product state engines.",
                    "focus_keywords": ["qiskit", "cirq", "statevector-simulation", "openqasm"]
                },
                {
                    "subdiscipline_id": "sub-09-02",
                    "title": "Quantum Machine Learning & Variational Algorithms",
                    "description": "Hybrid quantum-classical optimization for combinatorial problems and parameterized quantum circuits.",
                    "focus_keywords": ["pennylane", "vqe", "qaoa", "parameterized-circuits"]
                },
                {
                    "subdiscipline_id": "sub-09-03",
                    "title": "Quantum Error Correction (QEC) & Surface Codes",
                    "description": "Topological rotated surface codes, stabilizer measurements, and minimum-weight perfect matching decoders.",
                    "focus_keywords": ["quantum-error-correction", "surface-code", "syndrome-extraction", "mwpm-decoder"]
                },
                {
                    "subdiscipline_id": "sub-09-04",
                    "title": "Quantum Hamiltonian & Molecular Simulation",
                    "description": "Mapping fermionic molecular orbitals to qubit operators (Jordan-Wigner) for materials research.",
                    "focus_keywords": ["jordan-wigner", "hamiltonian-simulation", "quantum-chemistry"]
                }
            ],
            "adjacent_categories": [8, 10, 11, 16, 32]
        },
        "cross_category_tags": ["tag-quantum-technologies", "tag-high-performance-computing"]
    },
    10: {
        "category_id": 10,
        "stable_id": "cat-10-superconductivity-cryogenics",
        "title": "Superconducting Systems, Cryogenics & Energy Storage (SMES)",
        "short_title": "Superconducting Systems & Cryogenics",
        "slug": "10_superconducting_systems_cryoge.md",
        "markdown_file": "categories/10_superconducting_systems_cryoge.md",
        "meta_domain_id": "meta-hardware-quantum-physics",
        "domain_boundaries": {
            "definition": "High- and low-temperature superconductivity simulation, Ginzburg-Landau and London vortex dynamics, cryogenic thermal refrigeration cycles, and Superconducting Magnetic Energy Storage (SMES) systems.",
            "inclusions": [
                "Time-dependent Ginzburg-Landau (TDGL) superconducting vortex solvers",
                "High-temperature superconducting (HTS) tape and coil electromagnetic modeling",
                "Superconducting Magnetic Energy Storage (SMES) power conditioning systems",
                "Dilution refrigeration, pulse tube cryocoolers, and cryogenic heat transfer",
                "Josephson junction weak-link modeling and superconducting flux logic",
                "Critical current density (Jc) and magnetic flux pinning simulations"
            ],
            "exclusions": [
                {
                    "topic": "Solid oxide fuel cells and chemical battery degradation",
                    "redirect_category_id": 13,
                    "redirect_category_name": "Clean Energy, Solid Oxide Fuel Cells, Batteries & Power Grids",
                    "rationale": "Chemical battery modeling and fuel cells belong to category 13."
                },
                {
                    "topic": "High-level quantum algorithmic circuit synthesis",
                    "redirect_category_id": 9,
                    "redirect_category_name": "Quantum Computing, Quantum Algorithms, Circuit Simulation & Error Correction",
                    "rationale": "Quantum algorithms and logic gates belong to category 09."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 9,
                    "adjacent_category_name": "Quantum Computing, Quantum Algorithms, Circuit Simulation & Error Correction",
                    "boundary_relation": "Provides cryogenic thermal margins and superconducting ground planes for transmon qubits."
                },
                {
                    "adjacent_category_id": 12,
                    "adjacent_category_name": "Nuclear Fusion, Plasma Physics, Tokamaks & Particle Accelerators",
                    "boundary_relation": "Designs high-field toroidal and poloidal field HTS magnets for tokamak plasma confinement."
                }
            ]
        },
        "keywords": {
            "primary": ["superconductivity", "cryogenics", "smes", "hts", "josephson-junction", "vortex-dynamics", "ginzburg-landau", "thermal-modeling"],
            "secondary": ["dilution-refrigerator", "flux-pinning", "critical-current", "london-equations", "squid", "cryocooler", "superconducting-magnets"],
            "tools_and_frameworks": ["pyGL", "SuperPower-HTS", "CryoPy", "FreeFEM-TDGL", "COMSOL-Superconducting-Modules"],
            "architectural_patterns": ["Time-Dependent Ginzburg-Landau Finite Difference Integration", "Cryogenic Thermal Network Resistor Modeling", "Biot-Savart Magnetic Field Integration", "Nonlinear Power-Law E-J Constitutive Solving"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-hardware-quantum-physics",
            "parent_meta_domain_name": "Semiconductors, Quantum Systems & Applied Physics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-10-01",
                    "title": "Superconducting Vortex Dynamics & Ginzburg-Landau Solvers",
                    "description": "Simulation of magnetic flux quantum penetration, Abrikosov vortex lattices, and pinning center kinetics.",
                    "focus_keywords": ["ginzburg-landau", "abrikosov-vortex", "flux-pinning", "tdgl"]
                },
                {
                    "subdiscipline_id": "sub-10-02",
                    "title": "Cryogenic Refrigeration & Heat Exchanger Modeling",
                    "description": "Thermodynamic modeling of Gifford-McMahon, pulse tube, and helium-3/helium-4 dilution cooling stages.",
                    "focus_keywords": ["dilution-refrigeration", "pulse-tube", "cryogenic-heat-transfer", "sub-kelvin"]
                },
                {
                    "subdiscipline_id": "sub-10-03",
                    "title": "Superconducting Magnetic Energy Storage (SMES)",
                    "description": "High-inductance superconducting coils delivering millisecond dynamic grid stabilization and pulsed power.",
                    "focus_keywords": ["smes", "energy-storage", "pulsed-power", "grid-stabilization"]
                },
                {
                    "subdiscipline_id": "sub-10-04",
                    "title": "High-Field Superconducting Magnets & HTS Tapes",
                    "description": "Electromechanical stress analysis and quench protection for second-generation REBCO superconducting tapes.",
                    "focus_keywords": ["hts-magnets", "rebco-tape", "quench-protection", "lorentz-stress"]
                }
            ],
            "adjacent_categories": [9, 11, 12, 13]
        },
        "cross_category_tags": ["tag-quantum-technologies", "tag-computational-physics"]
    },
    11: {
        "category_id": 11,
        "stable_id": "cat-11-spintronics-micromagnetics",
        "title": "Spintronics, Micromagnetics & Atomistic Spin Dynamics (LLG)",
        "short_title": "Spintronics & Micromagnetics",
        "slug": "11_spintronics_micromagnetics_ato.md",
        "markdown_file": "categories/11_spintronics_micromagnetics_ato.md",
        "meta_domain_id": "meta-hardware-quantum-physics",
        "domain_boundaries": {
            "definition": "Landau-Lifshitz-Gilbert (LLG) equation solvers, micromagnetic finite-difference simulations, magnetic skyrmion dynamics, spin-transfer torque (STT/SOT), and spintronic non-volatile memory architectures.",
            "inclusions": [
                "Micromagnetic numerical simulation platforms (Mumax3, OOMMF, Fidimag)",
                "Landau-Lifshitz-Gilbert (LLG) integration and damping solvers",
                "Topological magnetic skyrmions, chiral domain walls, and hopfions",
                "Spin-Transfer Torque (STT) and Spin-Orbit Torque (SOT) memory devices (MRAM)",
                "Atomistic spin dynamics and magnonic spin-wave dispersion modeling",
                "Dzyaloshinskii-Moriya Interaction (DMI) and demagnetizing tensor calculations"
            ],
            "exclusions": [
                {
                    "topic": "Silicon ASIC standard cell physical routing",
                    "redirect_category_id": 8,
                    "redirect_category_name": "Semiconductor, Silicon EDA, RTL-to-GDSII, FPGA & RISC-V Architecture",
                    "rationale": "Classical CMOS routing and digital logic belong to category 08."
                },
                {
                    "topic": "Macroscopic electric motor electromagnetic FEM",
                    "redirect_category_id": 13,
                    "redirect_category_name": "Clean Energy, Solid Oxide Fuel Cells, Batteries & Power Grids",
                    "rationale": "Macroscopic electrical machine modeling belongs to clean energy/grid category 13."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 8,
                    "adjacent_category_name": "Semiconductor, Silicon EDA, RTL-to-GDSII, FPGA & RISC-V Architecture",
                    "boundary_relation": "Provides compact spice models for non-volatile magnetic tunnel junction (MTJ) cells."
                },
                {
                    "adjacent_category_id": 10,
                    "adjacent_category_name": "Superconducting Systems, Cryogenics & Energy Storage (SMES)",
                    "boundary_relation": "Explores superconducting-ferromagnetic heterostructures and triplet Cooper pairing."
                }
            ]
        },
        "keywords": {
            "primary": ["spintronics", "micromagnetics", "mumax3", "oommf", "llg-equation", "skyrmions", "spin-torque", "magnetism", "spin-dynamics"],
            "secondary": ["stt-mram", "spin-orbit-torque", "dzyaloshinskii-moriya", "magnonics", "domain-walls", "demagnetizing-field", "spin-wave"],
            "tools_and_frameworks": ["mumax/3", "oommf/oommf", "computationalmodelling/fidimag", "spirit-code/spirit"],
            "architectural_patterns": ["Landau-Lifshitz-Gilbert Runge-Kutta 4th Order Time Integration", "Fast Fourier Transform Convolution Demagnetizing Field Acceleration", "Dzyaloshinskii-Moriya Finite Difference Boundary Treatment", "Atomistic Heisenberg Spin Hamiltonian Mapping"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-hardware-quantum-physics",
            "parent_meta_domain_name": "Semiconductors, Quantum Systems & Applied Physics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-11-01",
                    "title": "GPU Micromagnetic Solvers & LLG Integration",
                    "description": "CUDA-accelerated spatial finite-difference magnetization dynamics solvers tracking precession and damping.",
                    "focus_keywords": ["mumax3", "oommf", "llg-solver", "demag-tensor"]
                },
                {
                    "subdiscipline_id": "sub-11-02",
                    "title": "Topological Magnetic Skyrmions & Chiral Textures",
                    "description": "Non-trivial topological spin textures stabilized by chiral interactions for ultra-dense race-track memories.",
                    "focus_keywords": ["skyrmions", "dmi-interaction", "chiral-domain-walls", "topological-charge"]
                },
                {
                    "subdiscipline_id": "sub-11-03",
                    "title": "Spin-Torque MRAM & Spintronic Neuromorphic Devices",
                    "description": "Spin-transfer torque switching mechanisms and spintronic oscillatory neurons for brain-inspired computing.",
                    "focus_keywords": ["stt-mram", "sot-mram", "spin-hall-effect", "spintronic-neurons"]
                },
                {
                    "subdiscipline_id": "sub-11-04",
                    "title": "Magnonics & Spin-Wave Dispersion",
                    "description": "Wave dynamics of collective spin excitations in patterned magnetic waveguides for zero-Joule-heating logic.",
                    "focus_keywords": ["magnonics", "spin-waves", "spin-wave-dispersion", "yig-waveguides"]
                }
            ],
            "adjacent_categories": [8, 9, 10, 28]
        },
        "cross_category_tags": ["tag-computational-physics", "tag-quantum-technologies"]
    },
    12: {
        "category_id": 12,
        "stable_id": "cat-12-nuclear-fusion-plasma",
        "title": "Nuclear Fusion, Plasma Physics, Tokamaks & Particle Accelerators",
        "short_title": "Nuclear Fusion & Plasma Physics",
        "slug": "12_nuclear_fusion_plasma_physics_.md",
        "markdown_file": "categories/12_nuclear_fusion_plasma_physics_.md",
        "meta_domain_id": "meta-hardware-quantum-physics",
        "domain_boundaries": {
            "definition": "Magnetic confinement fusion, Grad-Shafranov equilibrium solvers, magnetohydrodynamics (MHD) plasma stability, Particle-in-Cell (PIC) kinetic simulations, and particle accelerator beam dynamics.",
            "inclusions": [
                "Tokamak and stellarator magnetic equilibrium solvers (Grad-Shafranov)",
                "Magnetohydrodynamics (MHD) plasma stability and disruption modeling",
                "Kinetic Particle-in-Cell (PIC) electromagnetic plasma codes (SMILEI, EPOCH)",
                "Particle accelerator beam optics and synchrotron storage ring dynamics",
                "Plasma divertor scrape-off layer heat flux and neutral transport",
                "Laser-plasma wakefield acceleration and relativistic optics"
            ],
            "exclusions": [
                {
                    "topic": "Geological deep nuclear waste repository isolation",
                    "redirect_category_id": 22,
                    "redirect_category_name": "Subsurface Geomechanics, Geothermal (EGS) & Nuclear Waste Vitrification",
                    "rationale": "Subsurface waste storage and glass vitrification belong to category 22."
                },
                {
                    "topic": "Un-ionized aerodynamic fluid flow around wings",
                    "redirect_category_id": 17,
                    "redirect_category_name": "Aerospace Aerodynamics, Hypersonics & Rarefied Gas Dynamics",
                    "rationale": "Neutral gas aerospace aerodynamics belongs to category 17."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 10,
                    "adjacent_category_name": "Superconducting Systems, Cryogenics & Energy Storage (SMES)",
                    "boundary_relation": "Couples plasma equilibrium field coils to high-temperature superconducting magnet circuits."
                },
                {
                    "adjacent_category_id": 18,
                    "adjacent_category_name": "Computational Fluid Dynamics (CFD), Turbulence & Multiphase Slosh",
                    "boundary_relation": "Exchanges turbulence closures and spectral boundary methods with continuum fluid dynamics."
                }
            ]
        },
        "keywords": {
            "primary": ["nuclear-fusion", "plasma-physics", "tokamak", "mhd", "particle-in-cell", "particle-accelerators", "stellarator", "fusion-energy"],
            "secondary": ["grad-shafranov", "plasma-equilibrium", "smilei", "beam-dynamics", "divertor", "pic-simulation", "cyclotron", "laser-plasma"],
            "tools_and_frameworks": ["SmileiPIC/Smilei", "Warpx-project/WarpX", "OPAL-project/OPAL", "openfoam-plasma", "FreeGS"],
            "architectural_patterns": ["Grad-Shafranov Non-Linear Boundary Value Poisson Solving", "Yee Lattice Maxwell-Vlasov Particle-in-Cell Stepping", "Fokker-Planck Collision Operator Splitting", "Symplectic Accelerator Beam Tracking Integration"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-hardware-quantum-physics",
            "parent_meta_domain_name": "Semiconductors, Quantum Systems & Applied Physics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-12-01",
                    "title": "Tokamak Plasma Equilibrium & MHD Stability",
                    "description": "Axisymmetric Grad-Shafranov equilibrium solutions and neoclassical tearing mode stability modeling.",
                    "focus_keywords": ["grad-shafranov", "tokamak-equilibrium", "mhd-instabilities", "safety-factor-q"]
                },
                {
                    "subdiscipline_id": "sub-12-02",
                    "title": "Kinetic Particle-in-Cell (PIC) Plasma Solvers",
                    "description": "Relativistic kinetic solvers tracking charged macro-particles on electromagnetic spatial grids.",
                    "focus_keywords": ["warpx", "smilei", "pic-code", "vlasov-maxwell"]
                },
                {
                    "subdiscipline_id": "sub-12-03",
                    "title": "Particle Accelerator Beam Optics & Tracking",
                    "description": "High-brightness relativistic charged particle beam transfer lines, synchrotrons, and RF cavity linacs.",
                    "focus_keywords": ["accelerator-physics", "beam-dynamics", "synchrotron", "rf-cavity"]
                },
                {
                    "subdiscipline_id": "sub-12-04",
                    "title": "Stellarator 3D Magnetic Geometry Optimization",
                    "description": "Non-axisymmetric quasisymmetric magnetic field design and coil winding synthesis for steady-state fusion.",
                    "focus_keywords": ["stellarator", "quasisymmetry", "coil-optimization", "simsopt"]
                }
            ],
            "adjacent_categories": [10, 16, 17, 18]
        },
        "cross_category_tags": ["tag-computational-physics", "tag-high-performance-computing"]
    },
    13: {
        "category_id": 13,
        "stable_id": "cat-13-clean-energy-batteries",
        "title": "Clean Energy, Solid Oxide Fuel Cells, Batteries & Power Grids",
        "short_title": "Clean Energy, Batteries & Fuel Cells",
        "slug": "13_clean_energy_solid_oxide_fuel_.md",
        "markdown_file": "categories/13_clean_energy_solid_oxide_fuel_.md",
        "meta_domain_id": "meta-aerospace-energy-mechanics",
        "domain_boundaries": {
            "definition": "Electrochemical energy conversion and storage, Doyle-Fuller-Newman (DFN/P2D) lithium-ion battery modeling, solid oxide and PEM fuel cell thermodynamics, and electric grid distribution power flow simulation.",
            "inclusions": [
                "Physics-based battery electrochemical models (PyBaMM, DFN, SPM)",
                "Solid Oxide Fuel Cell (SOFC) and PEM fuel cell multi-physics solvers",
                "Electric distribution power flow analysis (OpenDSS, GridCal, Pandapower)",
                "Battery degradation, solid electrolyte interphase (SEI), and thermal runaway modeling",
                "Renewable solar PV and wind generation dispatch simulations",
                "Battery Management System (BMS) state-of-charge (SoC) estimation algorithms"
            ],
            "exclusions": [
                {
                    "topic": "Superconducting magnetic coil energy storage (SMES)",
                    "redirect_category_id": 10,
                    "redirect_category_name": "Superconducting Systems, Cryogenics & Energy Storage (SMES)",
                    "rationale": "SMES coils and cryogenic physics belong to category 10."
                },
                {
                    "topic": "Smart grid SCADA industrial communications protocols",
                    "redirect_category_id": 31,
                    "redirect_category_name": "Industrial Automation, SCADA, PLC Ladder Logic, OPC-UA & Hardware Security",
                    "rationale": "Industrial SCADA protocols (IEC 60870, DNP3, Modbus) belong to category 31."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 31,
                    "adjacent_category_name": "Industrial Automation, SCADA, PLC Ladder Logic, OPC-UA & Hardware Security",
                    "boundary_relation": "Connects power grid state estimators to industrial RTUs and substations."
                },
                {
                    "adjacent_category_id": 22,
                    "adjacent_category_name": "Subsurface Geomechanics, Geothermal (EGS) & Nuclear Waste Vitrification",
                    "boundary_relation": "Integrates geothermal brine production with thermodynamic binary organic Rankine cycles."
                }
            ]
        },
        "keywords": {
            "primary": ["clean-energy", "pybamm", "battery-simulation", "fuel-cells", "power-grid", "opendss", "electrochemical", "solar-wind", "grid-modeling"],
            "secondary": ["sofc", "pemfc", "doyle-fuller-newman", "thermal-runaway", "pandapower", "power-flow", "sei-layer", "bms", "renewable-energy"],
            "tools_and_frameworks": ["pybamm-team/PyBaMM", "tshort/OpenDSS", "e2nIEE/pandapower", "SanPen/GridCal", "battmo/BattMo"],
            "architectural_patterns": ["Coupled Electrochemical-Thermal Partial Differential Equation Integration", "Newton-Raphson AC Power Flow Solving", "Porous Electrode Theory Concentration Polarization", "Equivalent Circuit Model Kalman Filter SoC Tracking"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-aerospace-energy-mechanics",
            "parent_meta_domain_name": "Aerospace, Clean Energy & Mechanics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-13-01",
                    "title": "Lithium-Ion & Solid-State Battery Modeling",
                    "description": "Electrochemical multi-scale modeling tracking lithium concentration gradients and Butler-Volmer kinetics.",
                    "focus_keywords": ["pybamm", "dfn-model", "solid-state-battery", "lithium-ion"]
                },
                {
                    "subdiscipline_id": "sub-13-02",
                    "title": "Fuel Cell Multi-Physics & Thermodynamics",
                    "description": "Electrochemical activation overpotential and water management in PEM and Solid Oxide fuel cells.",
                    "focus_keywords": ["fuel-cell", "sofc", "pemfc", "overpotential"]
                },
                {
                    "subdiscipline_id": "sub-13-03",
                    "title": "Electric Power Distribution Flow Simulation",
                    "description": "Radial and meshed distribution network AC power flow solving with distributed solar/wind generation.",
                    "focus_keywords": ["opendss", "pandapower", "power-flow", "voltage-regulation"]
                },
                {
                    "subdiscipline_id": "sub-13-04",
                    "title": "Battery Thermal Runaway & Lifetime Degradation",
                    "description": "Exothermic side reaction kinetics, SEI growth, and thermal propagation simulation in pack enclosures.",
                    "focus_keywords": ["thermal-runaway", "sei-layer", "battery-degradation", "pack-cooling"]
                }
            ],
            "adjacent_categories": [10, 18, 22, 29, 31]
        },
        "cross_category_tags": ["tag-earth-and-environment", "tag-computational-physics"]
    },
    14: {
        "category_id": 14,
        "stable_id": "cat-14-space-systems-astrodynamics",
        "title": "Space Systems, Orbital Astrodynamics, Satellite Tracking & Rocket Propulsion",
        "short_title": "Space Systems & Rocket Propulsion",
        "slug": "14_space_systems_orbital_astrodyn.md",
        "markdown_file": "categories/14_space_systems_orbital_astrodyn.md",
        "meta_domain_id": "meta-aerospace-energy-mechanics",
        "domain_boundaries": {
            "definition": "Celestial mechanics, orbital trajectory propagation, satellite ephemeris determination, multi-body gravitational mechanics, and chemical/electric rocket propulsion thermochemistry.",
            "inclusions": [
                "Space flight dynamics and orbit propagation (Orekit, poliastro, Tudat)",
                "Chemical equilibrium rocket combustion thermochemistry (NASA CEA)",
                "SGP4/SDP4 satellite orbit propagation from Two-Line Element (TLE) sets",
                "Interplanetary gravity-assist trajectory design and Lambert's problem solvers",
                "Launch vehicle multi-stage ascent trajectory optimization",
                "Electric propulsion plasma plume mechanics (Hall thruster diagnostics)"
            ],
            "exclusions": [
                {
                    "topic": "Spacecraft proximity docking and capture mechanisms",
                    "redirect_category_id": 15,
                    "redirect_category_name": "Spacecraft Proximity Operations, Docking & Deployable Structures",
                    "rationale": "Terminal rendezvous and contact docking belong to category 15."
                },
                {
                    "topic": "Atmospheric hypersonic aerodynamic shockwaves",
                    "redirect_category_id": 17,
                    "redirect_category_name": "Aerospace Aerodynamics, Hypersonics & Rarefied Gas Dynamics",
                    "rationale": "High-Mach atmospheric aerodynamics belongs to category 17."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 15,
                    "adjacent_category_name": "Spacecraft Proximity Operations, Docking & Deployable Structures",
                    "boundary_relation": "Provides co-planar phasing orbits prior to terminal proximity rendezvous maneuvers."
                },
                {
                    "adjacent_category_id": 17,
                    "adjacent_category_name": "Aerospace Aerodynamics, Hypersonics & Rarefied Gas Dynamics",
                    "boundary_relation": "Handoffs atmospheric re-entry state vectors to hypersonic continuum solvers."
                }
            ]
        },
        "keywords": {
            "primary": ["space-systems", "astrodynamics", "orekit", "poliastro", "rocket-propulsion", "orbital-mechanics", "satellite-tracking", "propulsion", "orbit"],
            "secondary": ["sgp4", "lambert-solver", "tudat", "gravity-assist", "tle", "ephemeris", "nasa-cea", "nozzle-sizing", "launch-vehicle"],
            "tools_and_frameworks": ["poliastro/poliastro", "CS-SI/Orekit", "tudat-team/tudat", "nasa/CEA", "brandon-rhodes/python-sgp4"],
            "architectural_patterns": ["Cowell Perturbed Numerical Orbit Integration", "Gibbs-Appell Celestial Multibody Equations", "Gibbs Free Energy Minimization Combustion Equilibrium", "Two-Point Boundary Value Lambert Problem Shooting"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-aerospace-energy-mechanics",
            "parent_meta_domain_name": "Aerospace, Clean Energy & Mechanics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-14-01",
                    "title": "Orbital Propagation & Astrodynamics",
                    "description": "High-precision orbit propagation modeling J2-J4 geopotential perturbations, solar radiation pressure, and third-body gravity.",
                    "focus_keywords": ["orekit", "poliastro", "orbit-propagation", "orbital-perturbations"]
                },
                {
                    "subdiscipline_id": "sub-14-02",
                    "title": "Rocket Propulsion Thermodynamics & Nozzle Flow",
                    "description": "Equilibrium chemical combustion, characteristic exhaust velocity (c*), and de Laval supersonic expansion.",
                    "focus_keywords": ["rocket-propulsion", "cea", "de-laval-nozzle", "combustion-thermodynamics"]
                },
                {
                    "subdiscipline_id": "sub-14-03",
                    "title": "Satellite Ephemeris Tracking & Conjunction Assessment",
                    "description": "Automated ingestion of NORAD TLEs, SGP4 propagation, and orbital debris collision probability screening.",
                    "focus_keywords": ["sgp4", "tle", "conjunction-assessment", "space-debris"]
                },
                {
                    "subdiscipline_id": "sub-14-04",
                    "title": "Interplanetary Trajectory & Mission Optimization",
                    "description": "Porkchop plots, patched-conic approximations, and low-thrust electric propulsion trajectory optimization.",
                    "focus_keywords": ["porkchop-plots", "lambert-solver", "interplanetary-transfer", "gravity-assist"]
                }
            ],
            "adjacent_categories": [7, 15, 16, 17]
        },
        "cross_category_tags": ["tag-autonomous-mobility", "tag-computational-physics"]
    },
    15: {
        "category_id": 15,
        "stable_id": "cat-15-spacecraft-proximity-docking",
        "title": "Spacecraft Proximity Operations, Docking & Deployable Structures",
        "short_title": "Spacecraft Proximity & Docking",
        "slug": "15_spacecraft_proximity_operation.md",
        "markdown_file": "categories/15_spacecraft_proximity_operation.md",
        "meta_domain_id": "meta-aerospace-energy-mechanics",
        "domain_boundaries": {
            "definition": "Relative spacecraft motion, Clohessy-Wiltshire (Hill's) rendezvous equations, autonomous terminal guidance and docking mechanisms, and deployable space structures/solar array kinematics.",
            "inclusions": [
                "Clohessy-Wiltshire (CW) and Tschauner-Hempel relative orbital dynamics",
                "Autonomous terminal rendezvous and docking (RVD) guidance algorithms",
                "Contact dynamics and latching kinetics of space docking mechanisms",
                "Deployable space structures (tape-springs, pantograph booms, origami solar arrays)",
                "Vision-based pose estimation for non-cooperative satellite capture",
                "Safety keep-out zones and collision avoidance maneuver (CAM) planning"
            ],
            "exclusions": [
                {
                    "topic": "Global orbital astrodynamics and interplanetary transfers",
                    "redirect_category_id": 14,
                    "redirect_category_name": "Space Systems, Orbital Astrodynamics, Satellite Tracking & Rocket Propulsion",
                    "rationale": "Macro orbital trajectories belong to space systems category 14."
                },
                {
                    "topic": "Terrestrial civil building structural engineering",
                    "redirect_category_id": 29,
                    "redirect_category_name": "Smart Cities, Building Information Modeling (BIM/IFC) & Urban Mobility",
                    "rationale": "Civil building BIM models belong to category 29."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 14,
                    "adjacent_category_name": "Space Systems, Orbital Astrodynamics, Satellite Tracking & Rocket Propulsion",
                    "boundary_relation": "Receives orbital insertion states to initiate relative approach corridors."
                },
                {
                    "adjacent_category_id": 6,
                    "adjacent_category_name": "Robotics, Humanoid Kinematics, Dynamics, Actuators & Physics Simulation",
                    "boundary_relation": "Shares robotic manipulator kinematics for orbital berthing arms."
                }
            ]
        },
        "keywords": {
            "primary": ["proximity-operations", "spacecraft-docking", "relative-navigation", "clohessy-wiltshire", "rendezvous", "deployable-structures", "space-mechanisms"],
            "secondary": ["hills-equations", "satellite-servicing", "berthing", "tape-spring", "rpo", "keep-out-zone", "contact-dynamics", "capture-mechanism"],
            "tools_and_frameworks": ["CW-Rendezvous-Sim", "OpenRVD", "DeployableTrussSim", "Orekit-Proximity-Extension", "SpaceRoboticsBench"],
            "architectural_patterns": ["Clohessy-Wiltshire State Transition Matrix Propagation", "Glideslope Approach Trajectory Guidance", "Non-Linear Contact Compliance Penalty Methods", "Geometric Non-Linear Truss Folding Kinematics"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-aerospace-energy-mechanics",
            "parent_meta_domain_name": "Aerospace, Clean Energy & Mechanics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-15-01",
                    "title": "Relative Orbital Dynamics & CW Equations",
                    "description": "Linearized Hill-Clohessy-Wiltshire state propagation modeling relative motion in the local-vertical local-horizontal (LVLH) frame.",
                    "focus_keywords": ["clohessy-wiltshire", "hills-equations", "lvlh-frame", "relative-motion"]
                },
                {
                    "subdiscipline_id": "sub-15-02",
                    "title": "Autonomous Rendezvous & Terminal Docking (RVD)",
                    "description": "Glideslope trajectory planning and closed-loop visual servoing for precision docking probe alignment.",
                    "focus_keywords": ["docking-guidance", "glideslope", "rendezvous", "visual-servoing"]
                },
                {
                    "subdiscipline_id": "sub-15-03",
                    "title": "Deployable Space Structures & Boom Kinematics",
                    "description": "Simulation of tape-spring self-deployment, solar sail unfurling, and flexible appendage latching dynamics.",
                    "focus_keywords": ["deployable-structures", "tape-spring", "solar-sail-deployment", "boom-kinematics"]
                },
                {
                    "subdiscipline_id": "sub-15-04",
                    "title": "Non-Cooperative Target Capture & Servicing",
                    "description": "Robotic grapple planning and angular momentum detumbling for defunct satellite on-orbit servicing.",
                    "focus_keywords": ["satellite-servicing", "on-orbit-capture", "detumbling", "space-robotics"]
                }
            ],
            "adjacent_categories": [6, 7, 14, 19]
        },
        "cross_category_tags": ["tag-autonomous-mobility", "tag-computational-physics"]
    },
    16: {
        "category_id": 16,
        "stable_id": "cat-16-gravitational-waves-metrology",
        "title": "Gravitational Wave Astronomy, Precision Metrology & Casimir Physics",
        "short_title": "Gravitational Waves & Metrology",
        "slug": "16_gravitational_wave_astronomy_p.md",
        "markdown_file": "categories/16_gravitational_wave_astronomy_p.md",
        "meta_domain_id": "meta-hardware-quantum-physics",
        "domain_boundaries": {
            "definition": "Laser interferometric gravitational wave detection, matched filtering of compact binary coalescences, quantum optomechanical metrology, and macroscopic Casimir force physics.",
            "inclusions": [
                "Gravitational wave strain time-series data analysis (PyCBC, GWpy, LALSuite)",
                "Interferometer laser optics simulation and noise budgeting (Finesse)",
                "Compact Binary Coalescence (CBC) waveform template generation",
                "Quantum optomechanics, squeezed light, and radiation pressure noise modeling",
                "Casimir force boundary value problem solvers for microcavities",
                "Laser frequency stabilization and optical cavity resonance controllers"
            ],
            "exclusions": [
                {
                    "topic": "Classical acoustic ultrasonic phased arrays",
                    "redirect_category_id": 23,
                    "redirect_category_name": "Acoustic Levitation, Acoustofluidics & Phased Array Manipulation",
                    "rationale": "Macroscopic fluid acoustic levitation belongs to category 23."
                },
                {
                    "topic": "General quantum computing circuit algorithms",
                    "redirect_category_id": 9,
                    "redirect_category_name": "Quantum Computing, Quantum Algorithms, Circuit Simulation & Error Correction",
                    "rationale": "Universal quantum algorithms belong to category 09."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 9,
                    "adjacent_category_name": "Quantum Computing, Quantum Algorithms, Circuit Simulation & Error Correction",
                    "boundary_relation": "Applies quantum state squeezing techniques to overcome standard quantum detection limits."
                },
                {
                    "adjacent_category_id": 14,
                    "adjacent_category_name": "Space Systems, Orbital Astrodynamics, Satellite Tracking & Rocket Propulsion",
                    "boundary_relation": "Assists space-based gravitational wave detectors (LISA) with orbital constellation formation flying."
                }
            ]
        },
        "keywords": {
            "primary": ["gravitational-waves", "pycbc", "gwpy", "metrology", "laser-interferometry", "casimir-effect", "astrophysics", "general-relativity"],
            "secondary": ["finesse", "lalsuite", "strain-data", "squeezed-light", "compact-binary", "waveform-template", "optomechanics", "noise-budget"],
            "tools_and_frameworks": ["gwastro/pycbc", "gwpy/gwpy", "gwoptics/finesse", "lalsuite/lalsuite", "casimir-solver"],
            "architectural_patterns": ["Frequency-Domain Matched Filter Convolution", "Heterodyne Optical Interferometer Phase Demodulation", "Quantum Shot Noise Squeezing Matrix Propagation", "Lifshitz Casimir Force Dielectric Integration"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-hardware-quantum-physics",
            "parent_meta_domain_name": "Semiconductors, Quantum Systems & Applied Physics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-16-01",
                    "title": "Gravitational Wave Matched Filtering & Analysis",
                    "description": "Strain time-frequency Q-transforms, matched-filter SNR optimization, and compact binary parameter estimation.",
                    "focus_keywords": ["pycbc", "gwpy", "matched-filter", "strain-analysis"]
                },
                {
                    "subdiscipline_id": "sub-16-02",
                    "title": "Interferometer Optics & Noise Budgeting",
                    "description": "Optical simulation of Fabry-Pérot arm cavities, seismic isolation transfer functions, and thermal noise models.",
                    "focus_keywords": ["finesse", "fabry-perot", "noise-budget", "laser-optics"]
                },
                {
                    "subdiscipline_id": "sub-16-03",
                    "title": "Quantum Optomechanics & Squeezed Light",
                    "description": "Sub-shot-noise metrology using frequency-dependent squeezed vacuum states to beat the standard quantum limit.",
                    "focus_keywords": ["squeezed-light", "quantum-optomechanics", "standard-quantum-limit", "radiation-pressure"]
                },
                {
                    "subdiscipline_id": "sub-16-04",
                    "title": "Casimir Physics & Micro-Cavity Quantum Electrodynamics",
                    "description": "Boundary quantum vacuum fluctuations, Lifshitz theory, and nanomechanical Casimir stiction modeling.",
                    "focus_keywords": ["casimir-effect", "vacuum-fluctuations", "lifshitz-theory", "mems-stiction"]
                }
            ],
            "adjacent_categories": [9, 10, 12, 14]
        },
        "cross_category_tags": ["tag-computational-physics", "tag-quantum-technologies"]
    },
    17: {
        "category_id": 17,
        "stable_id": "cat-17-aerospace-hypersonics",
        "title": "Aerospace Aerodynamics, Hypersonics & Rarefied Gas Dynamics",
        "short_title": "Aerodynamics & Hypersonics",
        "slug": "17_aerospace_aerodynamics_hyperso.md",
        "markdown_file": "categories/17_aerospace_aerodynamics_hyperso.md",
        "meta_domain_id": "meta-aerospace-energy-mechanics",
        "domain_boundaries": {
            "definition": "Compressible aerodynamics, high-enthalpy hypersonic boundary layers, shock-wave/boundary-layer interactions, and Direct Simulation Monte Carlo (DSMC) for rarefied gas regimes.",
            "inclusions": [
                "Compressible and supersonic aerodynamic flow solvers (SU2, OpenFOAM aero)",
                "High-enthalpy hypersonic shock-wave and aerothermodynamic modeling",
                "Direct Simulation Monte Carlo (DSMC) rarefied gas flow codes (dsmcFoam, SPARTA)",
                "Transonic aeroelastic flutter and wing structural response analysis",
                "Aerodynamic shape optimization via adjoint gradient techniques",
                "Boundary layer transition prediction in high-Mach regimes"
            ],
            "exclusions": [
                {
                    "topic": "Incompressible low-speed marine water hydrodynamics",
                    "redirect_category_id": 24,
                    "redirect_category_name": "Marine Hydrodynamics, Sonar Transducer Arrays & Ocean Engineering",
                    "rationale": "Water hydrodynamics and ship seakeeping belong to category 24."
                },
                {
                    "topic": "Rocket engine combustion chamber thermochemistry",
                    "redirect_category_id": 14,
                    "redirect_category_name": "Space Systems, Orbital Astrodynamics, Satellite Tracking & Rocket Propulsion",
                    "rationale": "Internal rocket engine combustion belongs to category 14."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 14,
                    "adjacent_category_name": "Space Systems, Orbital Astrodynamics, Satellite Tracking & Rocket Propulsion",
                    "boundary_relation": "Provides aerodynamic drag and heating coefficients for spacecraft atmospheric re-entry profiles."
                },
                {
                    "adjacent_category_id": 18,
                    "adjacent_category_name": "Computational Fluid Dynamics (CFD), Turbulence & Multiphase Slosh",
                    "boundary_relation": "Shares turbulence model closures (SST k-omega, Spalart-Allmaras) with generic CFD."
                }
            ]
        },
        "keywords": {
            "primary": ["aerodynamics", "hypersonics", "su2", "dsmc", "shock-waves", "compressible-flow", "aerospace", "aeroelasticity", "boundary-layer"],
            "secondary": ["sparta", "dsmcfoam", "aerothermodynamics", "re-entry", "shock-standoff", "spalart-allmaras", "adjoint-optimization", "high-mach"],
            "tools_and_frameworks": ["su2code/SU2", "sparta/sparta", "OpenFOAM/OpenFOAM-dev", "nasa/Cart3D"],
            "architectural_patterns": ["Roe/AUSM Upwind Shock-Capturing Finite Volume Discretization", "Direct Simulation Monte Carlo Molecular Collision Sampling", "Adjoint Continuous Formulation Gradient Surface Optimization", "Coupled Fluid-Structure Aeroelastic Time-Marching"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-aerospace-energy-mechanics",
            "parent_meta_domain_name": "Aerospace, Clean Energy & Mechanics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-17-01",
                    "title": "Compressible High-Speed CFD (SU2)",
                    "description": "Supersonic and transonic finite-volume Navier-Stokes solving with adjoint-driven aerodynamic design.",
                    "focus_keywords": ["su2", "compressible-flow", "supersonic", "adjoint-optimization"]
                },
                {
                    "subdiscipline_id": "sub-17-02",
                    "title": "Hypersonic Aerothermodynamics & Shock Physics",
                    "description": "High-enthalpy chemical non-equilibrium air kinetics, shock-wave standoff distance, and thermal protection sizing.",
                    "focus_keywords": ["hypersonics", "aerothermodynamics", "shock-wave", "re-entry-heating"]
                },
                {
                    "subdiscipline_id": "sub-17-03",
                    "title": "Rarefied Gas Dynamics & DSMC Solvers",
                    "description": "Stochastic particle simulation of high-Knudsen number flows in upper planetary atmospheres.",
                    "focus_keywords": ["dsmc", "sparta", "rarefied-gas", "knudsen-number"]
                },
                {
                    "subdiscipline_id": "sub-17-04",
                    "title": "Transonic Aeroelasticity & Flutter Analysis",
                    "description": "Coupled aerostructural instability prediction preventing catastrophic wing flutter oscillations.",
                    "focus_keywords": ["aeroelasticity", "flutter", "wing-dynamics", "fluid-structure-interaction"]
                }
            ],
            "adjacent_categories": [14, 18, 19]
        },
        "cross_category_tags": ["tag-computational-physics", "tag-high-performance-computing"]
    },
    18: {
        "category_id": 18,
        "stable_id": "cat-18-computational-fluid-dynamics",
        "title": "Computational Fluid Dynamics (CFD), Turbulence & Multiphase Slosh",
        "short_title": "Computational Fluid Dynamics (CFD)",
        "slug": "18_computational_fluid_dynamics_c.md",
        "markdown_file": "categories/18_computational_fluid_dynamics_c.md",
        "meta_domain_id": "meta-aerospace-energy-mechanics",
        "domain_boundaries": {
            "definition": "Incompressible and multiphase Navier-Stokes solvers, Reynolds-Averaged Navier-Stokes (RANS), Large Eddy Simulation (LES), Lattice Boltzmann Methods (LBM), and propellant slosh dynamics.",
            "inclusions": [
                "Open-source CFD platforms (OpenFOAM, Palabos, Gerris, Basilisk)",
                "Multiphase volume-of-fluid (VOF) interface tracking solvers",
                "Turbulence modeling (RANS k-epsilon, k-omega SST, LES Smagorinsky, DNS)",
                "Lattice Boltzmann Methods (LBM) for micro-scale and complex geometry flows",
                "Liquid propellant tank sloshing dynamics and baffle dampening",
                "Conjugate Heat Transfer (CHT) and thermal-fluid boundary modeling"
            ],
            "exclusions": [
                {
                    "topic": "Rarefied molecular hypersonic flow regimes",
                    "redirect_category_id": 17,
                    "redirect_category_name": "Aerospace Aerodynamics, Hypersonics & Rarefied Gas Dynamics",
                    "rationale": "High-Mach and DSMC rarefied flows belong to category 17."
                },
                {
                    "topic": "Blood flow within cardiovascular arterial networks",
                    "redirect_category_id": 26,
                    "redirect_category_name": "Healthcare, Computational Biomedicine, Drug Discovery & Molecular Modeling",
                    "rationale": "Cardiovascular hemodynamics belongs to biomedical category 26."
                }
            ],
            "interfaces": [
                {
                    "adjacent_category_id": 19,
                    "adjacent_category_name": "Peridynamics, Structural Mechanics, FEA & Non-Local Fracture",
                    "boundary_relation": "Exchanges surface traction and displacement fields in coupled fluid-structure interaction (FSI)."
                },
                {
                    "adjacent_category_id": 24,
                    "adjacent_category_name": "Marine Hydrodynamics, Sonar Transducer Arrays & Ocean Engineering",
                    "boundary_relation": "Supplies free-surface viscous flow boundary conditions for marine propeller cavitation."
                }
            ]
        },
        "keywords": {
            "primary": ["cfd", "openfoam", "fluid-dynamics", "turbulence", "lattice-boltzmann", "multiphase", "navier-stokes", "fluid-simulation", "les"],
            "secondary": ["palabos", "vof", "rans", "propellant-slosh", "k-omega-sst", "dns", "conjugate-heat-transfer", "incompressible"],
            "tools_and_frameworks": ["OpenFOAM/OpenFOAM-dev", "palabos/palabos", "basilisk-vof", "su2code/SU2"],
            "architectural_patterns": ["PIMPLE/SIMPLE Pressure-Velocity Coupling", "Algebraic/Geometric Volume-of-Fluid Interface Reconstruction", "Lattice Boltzmann Collision-Streaming BGK Operator", "Wall-Modeled Large Eddy Simulation"]
        },
        "parent_child_relationships": {
            "parent_meta_domain_id": "meta-aerospace-energy-mechanics",
            "parent_meta_domain_name": "Aerospace, Clean Energy & Mechanics",
            "subdisciplines": [
                {
                    "subdiscipline_id": "sub-18-01",
                    "title": "General Navier-Stokes & Volume-of-Fluid Solvers",
                    "description": "Finite volume pressure-velocity coupling engines tracking sharp interfaces between immiscible fluids.",
                    "focus_keywords": ["openfoam", "vof", "navier-stokes", "pimple-algorithm"]
                },
                {
                    "subdiscipline_id": "sub-18-02",
                    "title": "Lattice Boltzmann Methods (LBM)",
                    "description": "Mesoscopic particle distribution methods simulating hydrodynamics over complex porous media.",
                    "focus_keywords": ["palabos", "lattice-boltzmann", "lbm", "porous-media"]
                },
                {
                    "subdiscipline_id": "sub-18-03",
                    "title": "Turbulence Modeling (RANS, LES, DNS)",
                    "description": "High-fidelity resolving of chaotic turbulent energy cascades from large eddies to Kolmogorov micro-scales.",
                    "focus_keywords": ["les", "rans", "dns", "turbulence-modeling", "kolmogorov"]
                },
                {
                    "subdiscipline_id": "sub-18-04",
                    "title": "Propellant Sloshing Dynamics & Baffle Damping",
                    "description": "Nonlinear free-surface slosh tracking in aerospace rocket tanks subject to acceleration disturbances.",
                    "focus_keywords": ["sloshing", "propellant-tanks", "baffles", "liquid-slosh"]
                }
            ],
            "adjacent_categories": [13, 17, 19, 24]
        },
        "cross_category_tags": ["tag-computational-physics", "tag-high-performance-computing"]
    }
}
