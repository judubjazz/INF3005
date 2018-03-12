function animate({duration, draw, timing}) {

  let start = performance.now();

  requestAnimationFrame(function animate(time) {
    let timeFraction = (time - start) / duration;
    if (timeFraction > 1) timeFraction = 1;

    let progress = timing(timeFraction)

    draw(progress);

    if (timeFraction < 1) {
      requestAnimationFrame(animate);
    }

  });
}


// https://stackoverflow.com/questions/7264974/show-text-letter-by-letter
showText = (target, message, index, interval)=> {
    if (index < message.length) {
        $(target).append(message[index++]);
        setTimeout( ()=> {showText(target, message, index, interval);}, interval);
    }

};
