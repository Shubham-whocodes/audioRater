document.addEventListener("DOMContentLoaded", function() {

    const audio = document.getElementById('audio');
    const wordButtons = document.querySelectorAll('.word');

    wordButtons.forEach(button => {
    button.addEventListener('click', () => {
        const startTimestamp = parseFloat(button.getAttribute('time-start'));
        const endTimestamp = parseFloat(button.getAttribute('time-end'));
        playFromTo(startTimestamp, endTimestamp);
    });
    });

    function playFromTo(start, end) {
    audio.currentTime = start;
    audio.play();

    //   setTimeout(() => {
    //     audio.pause();
    //     audio.currentTime = start;
    //   }, (end - start) * 1000);
    }

});
