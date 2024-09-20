import Player as Player;
import Enemy as Enemy;
import Constants;

class KinematicSeek:
#Holdsthestaticdataforthecharacterandtarget
    character = Player.Player
    target = Enemy.Enemy
    #Holdsthemaximumspeedthecharactercantravel
    maxSpeed = Constants.PLAYER_SPEED;
    
    def getSteering(target, character, maxSpeed):
        #Createthestructureforoutput
        steering = KinematicSteeringOutput();
        #Getthedirectiontothetarget
        steering.velocity= target.position-character.position;

        #Thevelocityisalongthisdirection,atfullspeed
        steering.velocity.normalize();
        steering.velocity*=maxSpeed;

        #Faceinthedirectionwewanttomove
        character.orientation= getNewOrientation(character.orientation, steering.velocity);

        #Outputthesteering
        steering.rotation = 0;
        return steering;
    


