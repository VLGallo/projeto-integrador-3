
const COMMAND_DELAY = 1000; 


const commandsToDelay = ['click', 'type', 'clear', 'check', 'uncheck', 'select'];

commandsToDelay.forEach((command) => {
  Cypress.Commands.overwrite(command, (originalFn, ...args) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(originalFn(...args));
      }, COMMAND_DELAY);
    });
  });
});


import './commands';
