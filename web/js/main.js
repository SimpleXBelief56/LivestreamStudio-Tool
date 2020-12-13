// Wizard Form Handling

// Declare Variables
var tabNumber = 0;
var wizardFormTabs = document.querySelectorAll(".form-wizard-tab")

function getTabNumber(){
    console.log(tabNumber)
}

function Delay(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function swap(swapMotion){
    if(swapMotion == "F"){
        $(wizardFormTabs[tabNumber]).addClass("animate__animated animate__fadeOutLeft")
        await Delay(500);
        $(wizardFormTabs[tabNumber]).removeClass("wizard-active");
        $(wizardFormTabs[tabNumber+1]).addClass("animate__animated animate__fadeInRight")
        $(wizardFormTabs[tabNumber+1]).addClass("wizard-active")
    } else {
        $(wizardFormTabs[tabNumber]).addClass("animate__animated animate__fadeOutRight")
        await Delay(500);
        $(wizardFormTabs[tabNumber]).removeClass("wizard-active");
        $(wizardFormTabs[tabNumber-1]).addClass("animate__animated animate__fadeInLeft")
        $(wizardFormTabs[tabNumber-1]).addClass("wizard-active");
    }
}

async function changeTabNumber(buttonClicked){
    if(buttonClicked == "Next"){
        if(tabNumber > 2){
            $(".btn-next").removeClass("btn-show")
            $(".btn-next").addClass("btn-hide")
            console.log("[DEBUG]: Max Number")
            // tabNumber = 4;
        } else {
            if($(".btn-previous").hasClass("btn-hide") == true){
                $(".btn-previous").removeClass("btn-hide")
                $(".btn-previous").addClass("btn-show")
            }
            swap("F");
            await Delay(500);
            tabNumber++;
            if($(wizardFormTabs[tabNumber-1]).hasClass("animate__animated animate__fadeOutLeft")){
                $(wizardFormTabs[tabNumber-1]).removeClass("animate__animated animate__fadeOutLeft")
            }
            await Delay(900);
            if($(wizardFormTabs[tabNumber]).hasClass("animate__animated animate__fadeInRight")){
                $(wizardFormTabs[tabNumber]).removeClass("animate__animated animate__fadeInRight")
            }
        }
    } else {
        if(tabNumber == 0){
            tabNumber = 0;
        } else {
            if(tabNumber < 5){
                if($(".btn-next").hasClass("btn-hide") == true){
                    $(".btn-next").removeClass("btn-hide")
                }
            }
            if(tabNumber < 2){
                $(".btn-previous").removeClass("btn-show")
                $(".btn-previous").addClass("btn-hide")
            }
            if(tabNumber == 0){
                // await Delay(900);
                // if($(wizardFormTabs[tabNumber]).addClass("animate__animated animate__fadeInLeft")){
                //     $(wizardFormTabs[tabNumber]).addClass("animate__animated animate__fadeInLeft")
                // }
            }
            swap("R");
            await Delay(500);
            tabNumber--;
            if($(wizardFormTabs[tabNumber+1]).hasClass("animate__animated animate__fadeOutRight")){
                $(wizardFormTabs[tabNumber+1]).removeClass("animate__animated animate__fadeOutRight")
            }
            await Delay(900);
            if($(wizardFormTabs[tabNumber]).hasClass("animate__animated animate__fadeInLeft")){
                $(wizardFormTabs[tabNumber]).removeClass("animate__animated animate__fadeInLeft")
            }
        }
    }
    getTabNumber()
}

// JQuery

$(".btn-next").click(function(){
    changeTabNumber("Next");
})

$(".btn-previous").click(function(){
    changeTabNumber("Previous");
})

