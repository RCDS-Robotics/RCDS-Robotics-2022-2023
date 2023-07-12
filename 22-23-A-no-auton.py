import vex


#region configuration
#true/false alternation, declaring motors and ports
brain  = vex.Brain()
motor_rightFront  = vex.Motor(vex.Ports.PORT18, vex.GearSetting.RATIO18_1, False)
motor_rightBack  = vex.Motor(vex.Ports.PORT17, vex.GearSetting.RATIO18_1, False)
motor_leftFront  = vex.Motor(vex.Ports.PORT13, vex.GearSetting.RATIO18_1, True)
motor_leftBack = vex.Motor(vex.Ports.PORT14, vex.GearSetting.RATIO18_1, True)
motor_intake = vex.Motor(vex.Ports.PORT10, vex.GearSetting.RATIO18_1, False)
motor_indexer = vex.Motor(vex.Ports.PORT9, vex.GearSetting.RATIO18_1, True)
motor_flywheel = vex.Motor(vex.Ports.PORT1, vex.GearSetting.RATIO18_1, True)
motor_roller = vex.Motor(vex.Ports.PORT19, vex.GearSetting.RATIO18_1, True)
#FIX PNEUMATICS??
piston_right = vex.Pneumatics(brain.three_wire_port.a)
piston_left = vex.Pneumatics(brain.three_wire_port.b)
#Controller
con = vex.Controller(vex.ControllerType.PRIMARY)
#endregion config

con.set_deadband(10)

isSpinning = False
isReversing = False
isIntake = False
directionSpin = True
intakeFront = True
expand = False

piston_right.set(False)
piston_left.set(False)
piston_right.close()
piston_left.close()


#region actions

motor_intake.set_rotation(-10)
while True:
    
    #setting motors to 0
    motor_leftFront_power = 0
    motor_rightFront_power = 0
    motor_leftBack_power = 0
    motor_rightBack_power = 0
    motor_intake_power = 0
    motor_indexer_power = 0
    motor_flywheel_power = 0
    motor_roller_power = 0
    
    # axis3: Tank Drive
    # buttonL1: Forward
		
    move = con.axis3.position()
    steer = con.axis4.position()
    motor_left_power = 0
    motor_right_power = 0
    
    if move != 0 or steer != 0:
        motor_left_power = move - steer
    
    if move != 0 or steer != 0:
        motor_right_power = move + steer
    
    # switch direction
    if con.buttonB.pressing():
        directionSpin = False
    elif con.buttonA.pressing():
        directionSpin = True
    
    if directionSpin == True:
        move = con.axis3.position()
        steer = con.axis4.position()
        if move != 0 or steer != 0:
            motor_left_power = move - steer
        
        if move != 0 or steer != 0:
            motor_right_power = move + steer
    elif directionSpin == False:
        move = -(con.axis3.position())
        steer = con.axis4.position()
        if move != 0 or steer != 0:
            motor_left_power = move - steer
        
        if move != 0 or steer != 0:
            motor_right_power = move + steer


    #conveyorintake
    if con.buttonUp.pressing():
        isSpinning = True
    elif con.buttonDown.pressing():
        isSpinning = False
    
    if isSpinning:
        isReversing = False;
        motor_flywheel_power = -100
    elif isReversing:
        isSpinning = False;
        motor_flywheel_power = 30
    else:
        motor_flywheel_power = 0
        
    #baseintake
    if con.buttonR1.pressing():
        isIntake = True;
            
    elif con.buttonR2.pressing():
        isIntake = False;
    
    if con.buttonX.pressing():
        intakeFront = True;
    elif con.buttonY.pressing():
        intakeFront = False;
    
    if isIntake:
        if intakeFront:
            motor_intake_power = 100
        else:
            motor_intake_power = -100
            
    else:
       motor_intake_power = 0
       
    #indexer
    if con.buttonL1.pressing():
        motor_indexer_power = -35
            
    elif con.buttonL2.pressing():
        motor_indexer_power = +35
            
    else:
       motor_indexer_power = 0
       
    
    #roller
    if con.buttonRight.pressing():
        motor_roller_power = 100
    else:
        motor_roller_power = 0
        
    #expansion
    if con.buttonLeft.pressing():
        expand = True
    
    if expand == True:
        if con.buttonX.pressing():
            piston_right.open()
            piston_left.open()
        
        
    
    #spinningwheels
    motor_leftFront.spin(vex.DirectionType.FWD, motor_left_power) 
    motor_rightFront.spin(vex.DirectionType.FWD, motor_right_power)
    motor_leftBack.spin(vex.DirectionType.FWD, -motor_left_power)
    motor_rightBack.spin(vex.DirectionType.FWD, -motor_right_power)
    motor_intake.spin(vex.DirectionType.FWD, motor_intake_power)
    motor_indexer.spin(vex.DirectionType.FWD, motor_indexer_power)
    if motor_intake_power == 0 and motor_indexer_power == 0:
        motor_intake.stop(vex.BrakeType.HOLD)
        motor_indexer.stop(vex.BrakeType.HOLD)
    motor_flywheel.spin(vex.DirectionType.FWD, motor_flywheel_power)
    motor_roller.spin(vex.DirectionType.FWD, motor_roller_power)
