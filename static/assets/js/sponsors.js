// const prefix= "https://elasticbeanstalk-us-west-1-124449841478.s3.us-west-1.amazonaws.com/website-pictures/Sponsors/"
const prefix = "static/images/sponsors/"

const sponsors = [
    { name: "99.3 Radio", logoSrc: prefix + "99_3_Radio_layered.jpeg" },
    { name: "CG Law", logoSrc: prefix + "CGLaw-Logo.png" },
    { name: "Oxnard Family Circle", logoSrc: prefix + "oxnard_family_circle_logo.jpeg" },
    { name: "California Rural Legal Assistance, Inc.", logoSrc: prefix + "crla_logo.png"},
    { name: "Kids and Families Together", logoSrc: prefix + "kft-logo-2018-hometab-980x400.jpg"},
    { name: "Point of Love Foundation", logoSrc: prefix + "point_of_love.png"},
    { name: "All Saints Episcopal Church", logoSrc: prefix + "All_Saints_Episcopal_Church_Logo.png" },
    { name: "Bethel Oxnard Church", logoSrc: prefix + "Bethel_AME_logo.png" },
    { name: "HDFC", logoSrc: prefix + "Logo - HDFC.jpeg" },
    { name: "New Progressive Church", logoSrc: prefix + "New_Progressive_Church_Logo.jpeg" },
    { name: "Faith Mission Christian Fellowship Church", logoSrc: prefix + "faith_mission_logo.jpeg" },
    { name: "Grace Life Church", logoSrc: prefix + "grace_life_logo.jpeg" },
    { name: "New Directions", logoSrc: prefix + "new_directions_logo.jpeg" },
    { name: "Zion Living World Ministries", logoSrc: prefix + "zion_logo.jpeg" },
    { name: "Miracle Center of Ventura", logoSrc: prefix + "miracle_center_logo.jpeg" },
    { name: "James Storehouse", logoSrc: prefix + "JSH_Blue.png"},
];

// Function to create sponsor elements and append them to the container
function renderSponsors() {
    const sponsorContainer = document.getElementById("sponsorContainer");

    sponsors.forEach(sponsor => {
        const sponsorElement = document.createElement("a");
        sponsorElement.classList.add("image", "fit");
        sponsorElement.href = "/advertisers-tracking" + "?name=" + sponsor.name;
        sponsorElement.target = "_blank";

        const logoElement = document.createElement("img");
        logoElement.src = sponsor.logoSrc;
        logoElement.alt = sponsor.name;
        // logoElement.classList.add("sponsor-logo");

        sponsorElement.appendChild(logoElement);
        sponsorContainer.appendChild(sponsorElement);
    });
}

// Call the function to render sponsors when the page loads
window.onload = renderSponsors;
