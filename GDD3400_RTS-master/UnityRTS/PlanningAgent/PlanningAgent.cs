﻿using System.Collections.Generic;
using System.Linq;
using GameManager.EnumTypes;
using GameManager.GameElements;
using UnityEngine;
using System;
using UnityEngine.Playables;
using static UnityEngine.UI.GridLayoutGroup;
using System.Diagnostics.Tracing;
using System.Diagnostics.Eventing.Reader;
using System.Linq.Expressions;

/////////////////////////////////////////////////////////////////////////////
// This is the Moron Agent
/////////////////////////////////////////////////////////////////////////////

namespace GameManager
{
    ///<summary>Planning Agent is the over-head planner that decided where
    /// individual units go and what tasks they perform.  Low-level 
    /// AI is handled by other classes (like pathfinding).
    ///</summary> 
    public class PlanningAgent : Agent
    {
        /// <summary>
        /// Enum for different states
        /// </summary>
        private enum PlayerState
        {
            Idle,
            Base,
            Army,
            Attack
        }
        //Set first state to idle
        PlayerState actualPlayerState = PlayerState.Idle;
        #region Private Data

        ///////////////////////////////////////////////////////////////////////
        // Handy short-cuts for pulling all of the relevant data that you
        // might use for each decision.  Feel free to add your own.
        ///////////////////////////////////////////////////////////////////////

        /// <summary>
        /// The enemy's agent number
        /// </summary>
        private int enemyAgentNbr { get; set; }

        /// <summary>
        /// My primary mine number
        /// </summary>
        private int mainMineNbr { get; set; }

        /// <summary>
        /// My primary base number
        /// </summary>
        private int mainBaseNbr { get; set; }

        /// <summary>
        /// List of all the mines on the map
        /// </summary>
        private List<int> mines { get; set; }

        /// <summary>
        /// List of all of my workers
        /// </summary>
        private List<int> myWorkers { get; set; }

        /// <summary>
        /// List of all of my soldiers
        /// </summary>
        private List<int> mySoldiers { get; set; }

        /// <summary>
        /// List of all of my archers
        /// </summary>
        private List<int> myArchers { get; set; }

        /// <summary>
        /// List of all of my bases
        /// </summary>
        private List<int> myBases { get; set; }

        /// <summary>
        /// List of all of my barracks
        /// </summary>
        private List<int> myBarracks { get; set; }

        /// <summary>
        /// List of all of my refineries
        /// </summary>
        private List<int> myRefineries { get; set; }

        /// <summary>
        /// List of the enemy's workers
        /// </summary>
        private List<int> enemyWorkers { get; set; }

        /// <summary>
        /// List of the enemy's soldiers
        /// </summary>
        private List<int> enemySoldiers { get; set; }

        /// <summary>
        /// List of enemy's archers
        /// </summary>
        private List<int> enemyArchers { get; set; }

        /// <summary>
        /// List of the enemy's bases
        /// </summary>
        private List<int> enemyBases { get; set; }

        /// <summary>
        /// List of the enemy's barracks
        /// </summary>
        private List<int> enemyBarracks { get; set; }

        /// <summary>
        /// List of the enemy's refineries
        /// </summary>
        private List<int> enemyRefineries { get; set; }

        /// <summary>
        /// List of the possible build positions for a 3x3 unit
        /// </summary>
        private List<Vector3Int> buildPositions { get; set; }

        //private bool isBuildingState = false;
        //private bool isArmyState = false;
        //private bool isAttackState = false;

        //Heuristic values
        private float valueTrainSoldier = 0;
        private float valueTrainArcher = 0;
        private float valueBuildBase = 0;
        private float valueBuildBarracks = 0;
        private float valueBuildRefinery = 0;

        private float maxWorkers = 20;
        private float numWorkers = 0;


        /// <summary>
        /// Finds all of the possible build locations for a specific UnitType.
        /// Currently, all structures are 3x3, so these positions can be reused
        /// for all structures (Base, Barracks, Refinery)
        /// Run this once at the beginning of the game and have a list of
        /// locations that you can use to reduce later computation.  When you
        /// need a location for a build-site, simply pull one off of this list,
        /// determine if it is still buildable, determine if you want to use it
        /// (perhaps it is too far away or too close or not close enough to a mine),
        /// and then simply remove it from the list and build on it!
        /// This method is called from the Awake() method to run only once at the
        /// beginning of the game.
        /// </summary>
        /// <param name="unitType">the type of unit you want to build</param>
        public void FindProspectiveBuildPositions(UnitType unitType)
            {
            //Gets the entire map in case the entire map isn't a valid position.
            for (int i = 0; i < GameManager.Instance.MapSize.x; ++i)
            {
                for (int j = 0; j < GameManager.Instance.MapSize.y; ++j)
                {
                    // Construct a new point near the unit's position
                    //If the unit is not on a valid position it moves it slightly until there is a valid position
                    Vector3Int testGridPosition = new Vector3Int(i, j, 0);

                    // Test if that position can be used to build the unit
                    if (Utility.IsValidGridLocation(testGridPosition)
                        && GameManager.Instance.IsBoundedAreaBuildable(unitType, testGridPosition))
                    {
                        // If this position is buildable, add it to the list
                        buildPositions.Add(testGridPosition);
                    }
                }
            }
        }

        /// <summary>
        /// Build a building
        /// </summary>
        /// <param name="unitType"></param>
        public void BuildBuilding(UnitType unitType)
        {
            Debug.Log("this has been called");
            // For each worker
            foreach (int worker in myWorkers)
            {
                // Grab the unit we need for this function
                Unit unit = GameManager.Instance.GetUnit(worker);
                Debug.Log("this has been answered");
                Debug.Log(unit.GridPosition);
                // Make sure this unit actually exists and we have enough gold
                if (unit != null && Gold >= Constants.COST[unitType])
                {
                    SetMine(unit);
                    Unit mine = GameManager.Instance.GetUnit(mainMineNbr);
                    float distance = Vector3Int.Distance(mine.GridPosition, buildPositions[0]);
                    Vector3Int buildingPos = buildPositions[0];
                    // Find the closest build position to this worker's position (DUMB) and 
                    // build the base there
                    foreach (Vector3Int toBuild in buildPositions)
                    {
                        if (GameManager.Instance.IsBoundedAreaBuildable(UnitType.BASE, toBuild))
                        {
                            float currentDist = Vector3Int.Distance(mine.GridPosition, toBuild);
                            if (currentDist < distance)
                            {
                                distance = currentDist;
                                buildingPos = toBuild;
                            }
                        }
                    }
                    Build(unit, buildingPos, unitType);
                    return;
                }
            }
        }
        /// <summary>
        /// Sets the mine as the closest one
        /// </summary>
        private void SetMine(Unit worker)
        {
            //If there are any mines left set one as a temp main mine
            if (mines.Count > 0)
            {
                mainMineNbr = mines[0];
                return;
            }
            //Else if there are none
            else if (mines.Count == 0)
            {
                mainMineNbr = -1;
                return;
            }
            //Get both mine locations
            Unit mine0 = GameManager.Instance.GetUnit(mines[0]);
            Unit mine1 = GameManager.Instance.GetUnit(mines[1]);
            //Get the distance between the worker and these mines
            float dist0 = Vector3.Distance(worker.WorldPosition, mine0.WorldPosition);
            float dist1 = Vector3.Distance(worker.WorldPosition, mine1.WorldPosition);
            //Located the one closest to the worker and set that mine as the main one
            if (dist0 < dist1)
            {
                mainMineNbr = mines[0];
            }
            else
            {
                mainMineNbr = mines[1];
            }
        }

        /// <summary>
        /// Attack the enemy
        /// </summary>
        /// <param name="myTroops"></param>
        public void AttackEnemy(List<int> myTroops)
        {
            if (myTroops.Count > 0)
            {
                // For each of my troops in this collection
                foreach (int troopNbr in myTroops)
                {
                    
                    // If this troop is idle, give him something to attack
                    Unit troopUnit = GameManager.Instance.GetUnit(troopNbr);
                    
                    if (troopUnit.CurrentAction == UnitAction.IDLE)
                    {
                        // If there are barracks to attack
                        if (enemyBarracks.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemyBarracks[UnityEngine.Random.Range(0, enemyBarracks.Count)]));
                        }
                        // If there are bases to attack
                        else if (enemyBases.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemyBases[UnityEngine.Random.Range(0, enemyBases.Count)]));
                        }
                        // If there are archers to attack
                        else if (enemyArchers.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemyArchers[0]));
                        }
                        // If there are soldiers to attack
                        else if (enemySoldiers.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemySoldiers[0]));
                        }
                        // If there are workers to attack
                        else if (enemyWorkers.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemyWorkers[UnityEngine.Random.Range(0, enemyWorkers.Count)]));
                        }
                        // If there are refineries to attack
                        else if (enemyRefineries.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemyRefineries[UnityEngine.Random.Range(0, enemyRefineries.Count)]));
                        }
                    }
                }
            }
            /*
            else if (myTroops.Count > 0)
            {
                // Find a good rally point
                Vector3Int rallyPoint = Vector3Int.zero;
                foreach (Vector3Int toBuild in buildPositions)
                {
                    if (GameManager.Instance.IsBoundedAreaBuildable(UnitType.BASE, toBuild))
                    {
                        rallyPoint = toBuild;
                        // For each of my troops in this collection
                        foreach (int troopNbr in myTroops)
                        {
                            // If this troop is idle, give him something to attack
                            Unit troopUnit = GameManager.Instance.GetUnit(troopNbr);
                            if (troopUnit.CurrentAction == UnitAction.IDLE)
                            {
                                Move(troopUnit, rallyPoint);
                            }
                        }
                        break;
                    }
                }
            }*/
        }
        #endregion

        #region Public Methods

        /// <summary>
        /// Called at the end of each round before remaining units are
        /// destroyed to allow the agent to observe the "win/loss" state
        /// </summary>
        public override void Learn()
        {
            Debug.Log("Nbr Wins: " + AgentNbrWins);
            //Debug.Log("PlanningAgent::Learn");
        }

        /// <summary>
        /// Called before each match between two agents.  Matches have
        /// multiple rounds. 
        /// </summary>
        public override void InitializeMatch()
        {
            Debug.Log("Mine's: " + AgentName);
            //Debug.Log("PlanningAgent::InitializeMatch");
        }

        /// <summary>
        /// Called at the beginning of each round in a match.
        /// There are multiple rounds in a single match between two agents.
        /// </summary>
        public override void InitializeRound()
        {
            numWorkers = 0;
            //Debug.Log("PlanningAgent::InitializeRound");
            buildPositions = new List<Vector3Int>();

            FindProspectiveBuildPositions(UnitType.BASE);

            // Set the main mine and base to "non-existent"
            mainMineNbr = -1;
            mainBaseNbr = -1;

            // Initialize all of the unit lists
            mines = new List<int>();

            myWorkers = new List<int>();
            mySoldiers = new List<int>();
            myArchers = new List<int>();
            myBases = new List<int>();
            myBarracks = new List<int>();
            myRefineries = new List<int>();

            enemyWorkers = new List<int>();
            enemySoldiers = new List<int>();
            enemyArchers = new List<int>();
            enemyBases = new List<int>();
            enemyBarracks = new List<int>();
            enemyRefineries = new List<int>();
        }

        /// <summary>
        /// Updates the game state for the Agent - called once per frame for GameManager
        /// Pulls all of the agents from the game and identifies who they belong to
        /// </summary>
        public void UpdateGameState()
        {
            // Update the common resources
            mines = GameManager.Instance.GetUnitNbrsOfType(UnitType.MINE);

            // Update all of my unitNbrs
            myWorkers = GameManager.Instance.GetUnitNbrsOfType(UnitType.WORKER, AgentNbr);
            mySoldiers = GameManager.Instance.GetUnitNbrsOfType(UnitType.SOLDIER, AgentNbr);
            myArchers = GameManager.Instance.GetUnitNbrsOfType(UnitType.ARCHER, AgentNbr);
            myBarracks = GameManager.Instance.GetUnitNbrsOfType(UnitType.BARRACKS, AgentNbr);
            myBases = GameManager.Instance.GetUnitNbrsOfType(UnitType.BASE, AgentNbr);
            myRefineries = GameManager.Instance.GetUnitNbrsOfType(UnitType.REFINERY, AgentNbr);

            // Update the enemy agents & unitNbrs
            List<int> enemyAgentNbrs = GameManager.Instance.GetEnemyAgentNbrs(AgentNbr);
            if (enemyAgentNbrs.Any())
            {
                enemyAgentNbr = enemyAgentNbrs[0];
                enemyWorkers = GameManager.Instance.GetUnitNbrsOfType(UnitType.WORKER, enemyAgentNbr);
                enemySoldiers = GameManager.Instance.GetUnitNbrsOfType(UnitType.SOLDIER, enemyAgentNbr);
                enemyArchers = GameManager.Instance.GetUnitNbrsOfType(UnitType.ARCHER, enemyAgentNbr);
                enemyBarracks = GameManager.Instance.GetUnitNbrsOfType(UnitType.BARRACKS, enemyAgentNbr);
                enemyBases = GameManager.Instance.GetUnitNbrsOfType(UnitType.BASE, enemyAgentNbr);
                enemyRefineries = GameManager.Instance.GetUnitNbrsOfType(UnitType.REFINERY, enemyAgentNbr);
                Debug.Log("<color=red>Enemy gold</color>: " + GameManager.Instance.GetAgent(enemyAgentNbr).Gold);
            }
        }

        /// <summary>
        /// Update the GameManager - called once per frame
        /// </summary>
        public override void Update()
        {
            //Set up a timer
            UpdateGameState();
            // If we have at least one base, assume the first one is our "main" base
            if (myBases.Count > 0)
            {
                mainBaseNbr = myBases[0];
                //Debug.Log("BaseNbr " + mainBaseNbr);
                //Debug.Log("MineNbr " + mainMineNbr);
            }
            if (mines.Count == 1)
            {
                mainMineNbr = mines[0];
                return;
            }
            BaseBuilding();
            ArmyBuilding();
            AttackPhase();

            
            // For each worker
            foreach (int worker in myWorkers)
            {
                // Grab the unit we need for this function
                Unit unit = GameManager.Instance.GetUnit(worker);

                // Make sure this unit actually exists and is idle
                if (unit != null && unit.CurrentAction == UnitAction.IDLE && mainBaseNbr >= 0 && mainMineNbr >= 0)
                {
                    // Grab the mine
                    Unit mineUnit = GameManager.Instance.GetUnit(mainMineNbr);
                    Unit baseUnit = GameManager.Instance.GetUnit(mainBaseNbr);
                    if (mineUnit != null && baseUnit != null && mineUnit.Health > 0)
                    {
                        Gather(unit, mineUnit, baseUnit);
                    }
                }
            }
        }

        /// <summary>
        /// Build bases
        /// </summary>
        private void BaseBuilding()
        {
            //Heuristic
            valueBuildBase = 1 - myBases.Count;
            valueBuildBarracks = myBases.Count - myBarracks.Count + myRefineries.Count/3;
            valueBuildRefinery = (myBases.Count + myBarracks.Count)/2 - myRefineries.Count/2;

            //If base value is higher than other building values
            if(valueBuildBase > valueBuildBarracks && valueBuildBase > valueBuildRefinery)
            {
                Debug.Log("valueBuildBase Heuristic Works");
                // If we have enough gold build base
                if (Gold >= Constants.COST[UnitType.BASE])
                {
                    mainBaseNbr = -1;
                    Debug.Log("Building the base");
                    BuildBuilding(UnitType.BASE);
                }
            }
            //If barracks value is higher than other building values
            else if (valueBuildBarracks > valueBuildBase && valueBuildBarracks > valueBuildRefinery)
            {
                Debug.Log("valueBuildBarracks Heuristic Works");
                // If we have enough gold, build barracks
                if (Gold >= Constants.COST[UnitType.BARRACKS])
                {
                    BuildBuilding(UnitType.BARRACKS);
                    Debug.Log("Building the barracks");
                }
            }
            //If refinery value is higher than other building values
            else if (valueBuildRefinery > valueBuildBarracks && valueBuildRefinery > valueBuildBase)
            {
                Debug.Log("valueBuildRefinery Heuristic Works");
                // If we have enough gold, build refinery
                if (Gold >= Constants.COST[UnitType.REFINERY])
                {
                    Debug.Log("Building the refinery");
                    BuildBuilding(UnitType.REFINERY);
                }
            }
            // For each base, determine if it should train a worker
            foreach (int baseNbr in myBases)
            {
                // Get the base unit
                Unit baseUnit = GameManager.Instance.GetUnit(baseNbr);

                // If the base exists, is idle, we need a worker, and we have gold
                if (baseUnit != null && baseUnit.IsBuilt
                                     && baseUnit.CurrentAction == UnitAction.IDLE
                                     && Gold >= Constants.COST[UnitType.WORKER]
                                     && numWorkers < maxWorkers)
                {
                    numWorkers++;
                    Train(baseUnit, UnitType.WORKER);
                }
            }
        }

        private void ArmyBuilding()
        {
            valueTrainSoldier = 1 - mySoldiers.Count / 100;
            
            valueTrainArcher = mySoldiers.Count / 100;
            // For each barracks, determine if it should train a soldier or an archer
            foreach (int barracksNbr in myBarracks)
            {
                // Get the barracks
                Unit barracksUnit = GameManager.Instance.GetUnit(barracksNbr);
                if (valueTrainArcher >= valueTrainSoldier)
                {
                    Debug.Log("train archer value amount: " + valueTrainSoldier);
                    // If this barracks still exists, is idle, we need archers, and have gold
                    if (barracksUnit != null && barracksUnit.IsBuilt
                             && barracksUnit.CurrentAction == UnitAction.IDLE
                             && Gold >= Constants.COST[UnitType.ARCHER])
                    {
                        Train(barracksUnit, UnitType.ARCHER);
                    }
                }else if(valueTrainSoldier > valueTrainArcher)
                {
                    Debug.Log("train soldier value amount: " + valueTrainSoldier);
                    // If this barracks still exists, is idle, we need soldiers, and have gold
                    if (barracksUnit != null && barracksUnit.IsBuilt
                        && barracksUnit.CurrentAction == UnitAction.IDLE
                        && Gold >= Constants.COST[UnitType.SOLDIER])
                    {
                        Train(barracksUnit, UnitType.SOLDIER);
                    }
                }
            }
        }
        private void AttackPhase()
        {
            // For any troops, attack the enemy
            AttackEnemy(mySoldiers);
            AttackEnemy(myArchers);
        }
        #endregion
    }
}