/**
 * Interactive Piano with..."The Great Old One"!
 */

// Sound mapping for piano keys
const sound = {
  65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
  87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
  83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
  69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
  68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
  70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
  84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
  71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
  89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
  72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
  85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
  74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
  75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
  79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
  76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
  80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
  186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
};

// Get piano elements
const piano = document.getElementById('piano');
const awakeningOverlay = document.getElementById('awakeningOverlay');
const keys = document.querySelectorAll('.key');

// State variables
let isAwakened = false;
let keySequence = '';
const secretCode = 'weseeyou';
let pressedKeys = new Set();

/**
* Play sound for a given key code
* @param {number} keyCode - The key code to play sound for
*/
const playSound = (keyCode) => {
  if (isAwakened) return; // Don't play sounds after awakening
  
  const soundUrl = sound[keyCode];
  if (soundUrl) {
      const audio = new Audio(soundUrl);
      audio.play().catch(error => {
          console.error('Error playing sound:', error);
      });
  }
};

/**
* Add visual press effect to a key
* @param {number} keyCode - The key code to press
*/
const pressKey = (keyCode) => {
  if (isAwakened) return; // Don't respond after awakening
  
  const keyElement = document.querySelector(`[data-key="${keyCode}"]`);
  if (keyElement && !pressedKeys.has(keyCode)) {
      keyElement.classList.add('key--pressed');
      pressedKeys.add(keyCode);
  }
};

/**
* Remove visual press effect from a key
* @param {number} keyCode - The key code to release
*/
const releaseKey = (keyCode) => {
  const keyElement = document.querySelector(`[data-key="${keyCode}"]`);
  if (keyElement) {
      keyElement.classList.remove('key--pressed');
      pressedKeys.delete(keyCode);
  }
};

/**
* Check if the typed sequence matches the secret code
* @param {string} key - The key that was pressed
*/
const checkSecretSequence = (key) => {
  if (isAwakened) return;
  
  // Add key to sequence
  keySequence += key.toLowerCase();
  
  // Keep only the last n characters where n is the length of secret code
  if (keySequence.length > secretCode.length) {
      keySequence = keySequence.slice(-secretCode.length);
  }
  
  // Check if sequence matches
  if (keySequence === secretCode) {
      awakenTheGreatOldOne();
  }
};

/**
* Awaken the Great Old One - trigger the easter egg
*/
const awakenTheGreatOldOne = () => {
  isAwakened = true;
  
  // Fade out the piano and title
  piano.classList.add('piano--fading');
  const pianoTitle = document.querySelector('.piano__title');
  if (pianoTitle) {
      pianoTitle.classList.add('piano__title--fading');
  }
  
  // Show the awakening overlay
  setTimeout(() => {
      awakeningOverlay.classList.add('awakening-overlay--visible');
  }, 500);
  
  // Play creepy audio
  const creepyAudio = new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1');
  creepyAudio.play().catch(error => {
      console.error('Error playing creepy sound:', error);
  });
};

/**
* Handle keydown events for piano playing
*/
const handleKeyDown = (event) => {
  const keyCode = event.keyCode;
  
  // Prevent default behavior for keys we're using
  if (sound[keyCode]) {
      event.preventDefault();
  }
  
  // Check secret sequence
  checkSecretSequence(event.key);
  
  // Play sound and show visual feedback
  if (sound[keyCode]) {
      playSound(keyCode);
      pressKey(keyCode);
  }
};

/**
* Handle keyup events to remove visual effect
*/
const handleKeyUp = (event) => {
  const keyCode = event.keyCode;
  if (sound[keyCode]) {
      releaseKey(keyCode);
  }
};

/**
* Handle mouse clicks on piano keys
*/
const handleKeyClick = (event) => {
  if (isAwakened) return;
  
  const keyElement = event.currentTarget;
  const keyCode = parseInt(keyElement.getAttribute('data-key'));
  
  if (sound[keyCode]) {
      playSound(keyCode);
      
      // Visual feedback for click
      keyElement.classList.add('key--pressed');
      setTimeout(() => {
          keyElement.classList.remove('key--pressed');
      }, 150);
  }
};

/**
* Handle mouseover on piano to show key labels
*/
const handlePianoMouseOver = () => {};

// Event listeners
document.addEventListener('keydown', handleKeyDown);
document.addEventListener('keyup', handleKeyUp);
piano.addEventListener('mouseover', handlePianoMouseOver);

// Add click listeners to all keys
keys.forEach(key => {
  key.addEventListener('click', handleKeyClick);
});

// Prevent multiple key presses from repeating
document.addEventListener('keydown', (event) => {
  if (event.repeat) {
      event.preventDefault();
  }
});