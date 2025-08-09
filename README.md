# CAMELOT: Intelligent 5-DOF Robotic Manipulator with Game AI Engine

<div align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue" alt="Language">
  <img src="https://img.shields.io/badge/Platform-VREP%20Simulation-green" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Minimax%20%7C%20Alpha--Beta-orange" alt="AI">
  <img src="https://img.shields.io/badge/DOF-5%20Axis%20Arm-purple" alt="DOF">
  <img src="https://img.shields.io/badge/Theme-HAL%209000-red" alt="Theme">
</div>

---

<div align="center">
  <h3>🤖 "I'm sorry Dave, I'm afraid I can't let you win this game." 🤖</h3>
  
  ![Camelot](https://easonnyc.github.io/portfolio/assets/images/camelot.png)
  
  <p><em>An integrated robotics and AI system themed after the evil sentient computer HAL from "2001: A Space Odyssey"</em></p>
</div>

---

## 🎯 Project Overview

**CAMELOT** is a sophisticated integration of robotics and artificial intelligence, featuring a **5-degree-of-freedom robotic manipulator** capable of autonomous board game play. This project combines advanced AI algorithms with precise robotic control to create an engaging human-robot gaming experience.

The system demonstrates the seamless integration of:
- **Game AI Engine** with strategic decision-making capabilities
- **Robotic Manipulation** with real-time trajectory planning
- **Human-Computer Interaction** through an intuitive gaming interface

### 🏆 Academic Achievement
Completed as capstone projects for **two graduate-level courses** at NYU Tandon School of Engineering:
- **CS4613 - Artificial Intelligence** (Spring 2015)
- **EL5223 - Sensor-Based Robotics** (Spring 2017)

---

## 🛠️ Technical Implementation

### 🤖 Robotic Control System

| Component | Implementation |
|-----------|----------------|
| **Hardware Simulation** | 5-DOF articulated robotic arm with precision end-effector control |
| **Motion Planning** | 3D waypoint generation and trajectory optimization for piece manipulation |
| **Inverse Kinematics** | Mathematical models for accurate positioning and collision avoidance |
| **Real-time Control** | Integrated game logic with robotic control loops for seamless operation |

### 🧠 Artificial Intelligence Engine

#### Search Algorithms
- **Minimax** implementation with Alpha-Beta pruning for optimal move selection
- **Iterative Deepening** for enhanced computational efficiency
- **Local Move Ordering** to optimize search performance

#### Heuristic Evaluation System
- 🎯 **Goal Proximity Analysis** - Distance-based scoring for strategic positioning
- ♟️ **Piece Positioning Optimization** - Tactical piece placement evaluation
- ⚡ **Strategic Advantage Assessment** - Multi-factor game state evaluation
- 🗣️ **Personality System** - AI will verbally "brag" or "whine" based on game position

### 🏗️ Software Architecture

```
CAMELOT System Architecture
├── 🎮 Game Logic Module
│   ├── Board state management
│   ├── Move validation
│   └── Win condition detection
├── 🤖 AI Engine Module
│   ├── Minimax with Alpha-Beta pruning
│   ├── Heuristic evaluation functions
│   └── Move generation and ordering
├── 🦾 Robotic Control Module
│   ├── Inverse kinematics solver
│   ├── Trajectory planning
│   └── VREP API integration
└── 🖥️ User Interface Module
    ├── Interactive game board GUI
    ├── Real-time status monitoring
    └── Human-robot interaction controls
```

---

![Camelot](https://easonnyc.github.io/portfolio/assets/images/camelot2.png)

## 🎮 How to Play Camelot

Camelot combines elements of **checkers** with strategic goal-based gameplay:

### 🎯 Game Objective
There are **two ways to win**:
1. **🏴‍☠️ Capture Victory**: Eliminate all opponent pieces by jumping over them
2. **🥅 Goal Victory**: Move one of your pieces into the opponent's goal while defending your own

### 🕹️ Movement Rules

| Move Type | Description | Notation |
|-----------|-------------|----------|
| **Plain Move** | Move any piece one square in any direction to a free space | Standard move |
| **Cantor** | Jump over a friendly adjacent piece to the free space beyond | Friendly leap |
| **Capture** | Jump over an enemy piece (like checkers) and remove it | Enemy elimination |

### 🏁 Game Board
- Standard board with **goal tiles** at upper and lower ends
- Players alternate turns moving one piece at a time
- Strategic positioning near goals is crucial for victory

> **Note**: Official rules were modified to reduce search space complexity and create a viable semester-long project scope.

---

## 📹 Demo & Visualization

### 🎬 Video Demonstration
*Experience CAMELOT in action with AI decision-making and robotic manipulation*

[![Video of AI and VREP simulation footage for Camelot](http://i.imgur.com/pA487Rl.png)](http://www.youtube.com/watch?v=uc2t7ujrt4c "Youtube Clip: Artificial Intelligence and Robot ARM Demo for Camelot board game")

**Features Demonstrated:**
- Real-time AI vs Human gameplay
- Robotic arm piece manipulation in VREP simulation
- Strategic decision-making with verbal commentary
- 3D trajectory planning and execution

---

## 🔧 Technical Specifications

### Development Environment
- **Programming Language**: Python
- **Simulation Platform**: VREP (Virtual Robot Experimentation Platform)
- **Architecture**: Modular, object-oriented design with clean API boundaries

### AI Implementation
- **Search Algorithm**: Minimax with Alpha-Beta pruning
- **Optimization**: Iterative deepening and move ordering
- **Evaluation**: Multi-factor heuristic system
- **Performance**: Real-time decision making capabilities

### Robotic Control
- **Kinematics**: Forward/inverse kinematics implementation
- **Planning**: 3D trajectory optimization
- **Control**: Real-time servo positioning
- **Integration**: Seamless game-to-robot command translation

### Project Timeline
- **Duration**: Two academic semesters (developed iteratively)
- **Phase 1**: AI engine and game logic development
- **Phase 2**: Robotic integration and 3D simulation

---

## 💡 Competencies

### Technical Skills
- ✅ Advanced algorithm implementation and optimization
- ✅ Robotic system programming and control
- ✅ Real-time software development
- ✅ System integration and testing
- ✅ Mathematical modeling and problem-solving
- ✅ Human-computer interaction design

### Engineering Practices
- ✅ Modular software architecture
- ✅ API design and integration
- ✅ Error handling and robust operation
- ✅ Documentation and research analysis
- ✅ Academic project management

---

## 🎨 Project Inspiration & Credits

### 🎬 Thematic Inspiration
This project pays homage to **HAL 9000**, the iconic AI antagonist from Stanley Kubrick's "2001: A Space Odyssey," bringing the concept of an intelligent, game-playing computer to life through modern robotics and AI.

### 📚 Credits & Acknowledgments

| Component | Credit |
|-----------|--------|
| **Original Camelot Game** | Parker Brothers |
| **Literary Source** | "2001: A Space Odyssey" novel by Arthur C. Clarke |
| **Film Inspiration** | 1968 film directed and produced by Stanley Kubrick |
| **Game Graphics** | [Camelot (board game) - Wikipedia](https://en.wikipedia.org/wiki/Camelot_(board_game)) |
| **Audio Assets** | [WAV Source Movies](http://www.wavsource.com/movies/2001.htm) & [HAL 9000 Sounds](http://sounds.stoutman.com/sounds.php?Category=HAL%209000) |

---

## 📄 Usage & Distribution

> **⚠️ Important Notice**: This project and its elements are **strictly not intended for redistribution** of any kind, commercial or otherwise. This repository is maintained by the author for **academic and reference purposes only**.

### Academic Use
- Demonstrates advanced AI and robotics integration
- Suitable for educational research and reference
- Showcases interdisciplinary engineering project development

---

## 👨‍💻 Author

**Eason Smith** - Project Lead & Developer  
📧 [Eason@EasonRobotics.com](mailto:Eason@EasonRobotics.com)   
💼 [LinkedIn](https://linkedin.com/in/easonsmith)  

### Academic Institution
**New York University** - Tandon School of Engineering  
*Dual Degree B.S. in Electrical and Computer Engineering*

---

## 🚀 Technical Impact

CAMELOT represents a sophisticated fusion of artificial intelligence and robotics, including:

- **Real-time AI decision making** in complex game environments
- **Precise robotic manipulation** with trajectory optimization
- **Seamless human-robot interaction** through intuitive interfaces
- **Modular system architecture** enabling future enhancements

This project showcases the practical application of advanced algorithms in robotics, making it an excellent demonstration of skills relevant to **autonomous systems**, **game AI development**, and **human-robot interaction** in modern engineering applications.

---

<div align="center">
  <h3>🎯 "The game is afoot, Dave. Let's see if you can outmaneuver a machine." 🎯</h3>
</div>
