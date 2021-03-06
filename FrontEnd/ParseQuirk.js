function parseQuirk(obj) {
	//Determine what the weakness will be
	var finalLimit = limitCalc(obj["Power"]["Limit"],
		obj["Weak"]["Desc"],
		obj["Weak"]["URL"]);
	
	// Determines how the quirk will manifest
	var channel = activationCalc(obj["Body"],
		obj["action"],
		obj["activity"],
		obj["Power"]["Special"]);
	
	// generate a random range that affects the power, that trends towards lower values
	var min = 0;
	var max = 1000;
	var range = parseInt(min + (max - min) * Math.pow(Math.random(), 6));
	
	return constructOutput(obj["Power"]["Name"],
		obj["Power"]["Desc"],
		finalLimit,
		channel,
		range,
		obj["Power"]["Special"]);
	
}

// Creates the final format for the quirk to be displayed to the user
function constructOutput(powerName, powerDesc, finalLimit, channel, range, special) {
	title = "<div class='quirkCapsule'><h2 class='quirkHeader'>Quirk</h2><div class='quirkDiv'>" + powerName + "</div></div>";
	desc = "<div class='quirkCapsule'><h2 class='quirkHeader'>Info</h2><div class='quirkDiv'>" + powerDesc + "</div></div>";
	chnl = "<div class='quirkCapsule'><h2 class='quirkHeader'>Method of Activation</h2><div class='quirkDiv'>" + channel + "</div></div>";
	limit = "<div class='quirkCapsule'><h2 class='quirkHeader'>Limit / More Susceptible To</h2><div class='quirkDiv'>" + finalLimit.replace(' Symptoms and Signs','') + "</div></div>";
	rnge = "";
	
	if(!special.includes("No Range")) {
		rnge = "<div class='quirkCapsule'><h2 class='quirkHeader'>Range</h2><div class='quirkDiv'>" + range + "m</div></div>";
	}
	
	return title + desc + chnl + limit + rnge;
	
}

// Determine what the weakness will be.  If its the disease, the url for the
// page element will be set here
function limitCalc(limitPower, limitDisease, url) {
	var finalLimit = "";
	var limitChance = Math.random();
	
	if(limitPower == "None" || limitChance < 0.3) {
		finalLimit = "<a target='_blank' href=" + url + ">" + limitDisease + "</a>";
	} else {
		finalLimit = limitPower;
	}
	
	return finalLimit;
}

// Determines how the quirk is activated, whether body or certain activity
function activationCalc(body, action, activity, special) {
	var manifestation = "";
	var manChance = Math.random();
	
	if (special != null && special.includes("body")) {
		manifestation = manBodyPart(body, action);
	} else if(manChance < 0.3 || special.includes("activity")) {
		manifestation = activity.charAt(0).toUpperCase() + activity.slice(1);
	} else {
		manifestation = manBodyPart(body, action);;
	}
	
	return manifestation;
}

// Constructs the body part used for the quirk and if there's an extra step
// in activating the power.
function manBodyPart(body, action) {
	var bodyChance = Math.random();
	var bodyActivation = "";
	
	// gives a chance that the whole body could be the source of the quirk.
	// the website doesn't have whole body as an option 
	if(bodyChance < .1) {
		bodyActivation = "Whole body";
	} else {
		bodyActivation = body.charAt(0).toUpperCase() + body.slice(1);
	}
	
	// Adds an optional descriptor to the body part to be, for example, "'move' your arm"
	var extraDescriptor = Math.random();
	
	if(extraDescriptor < .3) {
		bodyActivation = action + " your " + bodyActivation;
	}
	
	return bodyActivation;
}

