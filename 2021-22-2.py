import vex

#region configuration
#true/false alternation, declaring motors and ports
brain  = vex.Brain()
motor_rightFront  = vex.Motor(vex.Ports.PORT10, vex.GearSetting.RATIO18_1, False)
motor_leftFront  = vex.Motor(vex.Ports.PORT1, vex.GearSetting.RATIO18_1, True)
motor_rightBack  = vex.Motor(vex.Ports.PORT20, vex.GearSetting.RATIO18_1, False)
motor_leftBack = vex.Motor(vex.Ports.PORT12, vex.GearSetting.RATIO18_1, True)
motor_intake1 = vex.Motor(vex.Ports.PORT4, vex.GearSetting.RATIO18_1, False)
motor_intake2 = vex.Motor(vex.Ports.PORT6, vex.GearSetting.RATIO18_1, True)
motor_ringIntake = vex.Motor(vex.Ports.PORT8, vex.GearSetting.RATIO18_1, True)
con = vex.Controller(vex.ControllerType.PRIMARY)
#endregion config

con.set_deadband(10)

isSpinning = False
directionSpin = True



#region actions

motor_intake1.set_rotation(-10)
motor_intake2.rotation(-10)
while True:
    
    #setting motors to 0
    motor_leftFront_power = 0
    motor_rightFront_power = 0
    motor_leftBack_power = 0
    motor_rightBack_power = 0
    motor_intake1_power = 0
    motor_intake2_power = 0
    motor_ringIntake_power = 0
    
    # axis3: Tank Drive
    # buttonL1: Forward
		
	# axis2: Linear Control (to change the way the motors work in proportion to the wheels, make the power negative)
    power=con.axis3.position()
    #if power !=0: (trying to do something with if statments and power - didnt really work - in some og code though)
    motor_right_power=power
    power=con.axis2.position()
    #if power !=0:
    motor_left_power=power
    
    # switch direction?
    if con.buttonB.pressing():
        directionSpin = False
    elif con.buttonA.pressing():
        directionSpin = True
    
    if directionSpin == True:
        # axis2: Linear Control (to change the way the motors work in proportion to the wheels, make the power negative)
        power=con.axis3.position()
        #if power !=0: (trying to do something with if statments and power - didnt really work - in some og code though)
        motor_right_power=power
        power=con.axis2.position()
        #if power !=0:
        motor_left_power=power
    elif directionSpin == False:
        # axis2: change to negative spin to change direction
        power = -(con.axis3.position())
        #if power !=0: (trying to do something with if statments and power - didnt really work - in some og code though)
        motor_left_power=power
        power = -(con.axis2.position())
        #if power !=0:
        motor_right_power=power

    
    #conveyorintake
    if con.buttonL1.pressing():
        # motor_ringIntake_power = -35
        isSpinning = True
    elif con.buttonL2.pressing():
        # motor_ringIntake_power = 35
        isSpinning = False
    else:
        pass
         # motor_ringIntake_power = 0
    """if con.buttonB.pressed(): trying to do something here with 
        motor_ringIntake_power = -50;
    if con.buttonX.pressed():
        motor_ringIntake_power = 0;"""
    #change power on green motor if needed for intake
    
    #baseintake
    if con.buttonR1.pressing():
        if motor_intake1.rotation() < -750:
            motor_intake1.stop()
        else:
            motor_intake1_power = -85
            
        if motor_intake2.rotation() < -750:
            motor_intake2.stop()
        else:
            motor_intake2_power = -85
            
        
         
        
    elif con.buttonR2.pressing():
        if motor_intake1.rotation() > 0:
            motor_intake1.stop()
        else:
            motor_intake1_power = +85
            
            
        if motor_intake2.rotation() > 0:
            motor_intake2.stop()
        else:
            motor_intake2_power = +85
            
            
    else:
       motor_intake1_power = 0
       motor_intake2_power = 0
        
        
    
    #spinningwheels
    motor_leftFront.spin(vex.DirectionType.FWD, motor_left_power) 
    motor_rightFront.spin(vex.DirectionType.FWD, motor_right_power)
    motor_leftBack.spin(vex.DirectionType.FWD, motor_left_power)
    motor_rightBack.spin(vex.DirectionType.FWD, motor_right_power)
    motor_intake1.spin(vex.DirectionType.FWD, motor_intake1_power)
    motor_intake2.spin(vex.DirectionType.FWD, motor_intake2_power)
    if motor_intake1_power == 0 and motor_intake2_power == 0:
        motor_intake1.stop(vex.BrakeType.HOLD)
        motor_intake2.stop(vex.BrakeType.HOLD)
    motor_ringIntake.spin(vex.DirectionType.FWD, -35 if isSpinning else 0)
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
