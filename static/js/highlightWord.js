document.addEventListener("DOMContentLoaded", function() {
    const audio = document.getElementById('audio');

    const wordSpans = document.querySelectorAll('.word');

    audio.addEventListener('timeupdate', function() {
    const currentTime = audio.currentTime;

    for (let i = 0; i < wordSpans.length; i++) {
        const start = parseFloat(wordSpans[i].getAttribute('time-start'));
        const end = parseFloat(wordSpans[i].getAttribute('time-end'));

        if (currentTime >= start && currentTime < end) {
            wordSpans[i].style.textDecoration = 'underline';
            // wordSpans[i].classList.add('underline');
        } else {
            wordSpans[i].style.textDecoration = 'none';
            // wordSpans[i].classList.remove('underline');
        }
    }
    });

    audio.addEventListener('ended', function() {
    for (let i = 0; i < wordSpans.length; i++) {
        wordSpans[i].style.textDecoration = 'none';
        // wordSpans[i].classList.remove('underline');
    }
    });
    function playFrom(time) {
    audio.currentTime = time;
    audio.play();
    }

});