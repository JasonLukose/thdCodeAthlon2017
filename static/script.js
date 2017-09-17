var fancyText = document.getElementById('fancy');
var intervalTime = 150;
var initialPause = 1000;
var callbackPause = 500;

//callback is function 
function deleteContent(callback) {
	/* setInterval(functionName, timeInms)*/
    var intervalId = setInterval(function() {
        if (fancyText.innerHTML.length == 0) {
        	/* intervalId is the number that allows clearInterval to stop the Interval*/
            clearInterval(intervalId);

            if (callback) {
                setTimeout(callback, callbackPause);
            }
        }

        fancyText.innerHTML = fancyText.innerHTML.substring(0, fancyText.innerHTML.length - 1);
    }, intervalTime);

}

// contentToAdd is a string
function addContent(contentToAdd, callback) {
    var currentIndex = 0;

    var intervalId = setInterval(function() {
        if (currentIndex == contentToAdd.length) {
            clearInterval(intervalId);

            if (callback) {
                setTimeout(callback, callbackPause);
            }
        }

        fancyText.innerHTML = contentToAdd.substring(0, currentIndex);
        currentIndex++;
    }, intervalTime);
}

setTimeout(function() {
    deleteContent(function() {
        addContent("fixing a fence", function() {
            deleteContent(function() {
                addContent("creating a weatherproof door", function() {
                    deleteContent(function() {
                        addContent("any project on your mind");
                    })
                });
            });
        });
    });
}, initialPause);
