/* Page-specific choreography. The vendored Scrollcraft engine remains unchanged. */
(() => {
  'use strict';
  document.documentElement.classList.add('has-js');

  const demo = document.querySelector('[data-demo]');
  if (!demo) return;
  const hero = document.querySelector('.sb-team-hero');
  const heroStage = hero.querySelector('[data-sc-stage]');
  const workflow = document.querySelector('#how-it-works');
  const stageSurface = workflow.querySelector('[data-sc-stage]');
  const stageButtons = [...demo.querySelectorAll('[data-stage]')];
  const scenarioButtons = [...demo.querySelectorAll('[data-scenario]')];
  const messages = [...demo.querySelectorAll('[data-message]')];
  const approval = document.querySelector('#approval-toggle');
  const announcement = demo.querySelector('[data-demo-announcement]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const desktop = matchMedia('(min-width: 1024px) and (min-height: 700px)');
  let scenario = 'booking';
  let step = 2;
  let engine = null;
  let heroPinned = false;
  let frame = 0;

  const examples = {
    booking: {
      title: 'From interest to booking',
      person: 'Guest',
      steps: ['An enquiry arrives', 'A helpful response', 'The right next step'],
      details: ['A guest asks about your property.', 'Your approved information supplies the answer.', 'A clear route to your booking engine.'],
      messages: ['“Would your place suit a family weekend?”', 'Your agent shares the family-friendly details, answers questions and follows up on the enquiry.', 'The guest gets a direct booking link to check dates and reserve.'],
      statuses: ['A potential guest has a question.', 'Useful answers, based on your property.', 'Interest has a clear next step.'],
      exception: ['“Could we check in early on Friday?”', 'Your agent checks the agreed guidance and flags the request for approval.', 'You or your team confirm what is possible before the guest receives a promise.']
    },
    social: {
      title: 'From a reason to stay to a ready-to-share post',
      person: 'Your plan',
      steps: ['A reason to stay', 'Content takes shape', 'You approve the post'],
      details: ['Give the right guests a reason to choose you.', 'Turn your property’s strengths into useful content.', 'Keep your channels active on your terms.'],
      messages: ['“Show couples why this is a great autumn escape.”', 'Your agent drafts a post and caption using your property details, photos and brand voice.', 'You review the content, then approved posts go into your publishing plan.'],
      statuses: ['Start with the guest you want to attract.', 'Your stay becomes something worth sharing.', 'Approved content, ready for your channels.'],
      exception: ['“Should this post include a last-minute discount?”', 'Your agent flags the pricing decision instead of adding an unapproved offer.', 'You choose the offer and approve the final post before it is scheduled.']
    },
    operations: {
      title: 'From a booking update to less chasing',
      person: 'Booking update',
      steps: ['A stay is coming up', 'The right reminders', 'Everyone knows the plan'],
      details: ['An agreed booking event starts the workflow.', 'Messages and tasks reach the right people.', 'Keep track of what still needs attention.'],
      messages: ['“The next guests arrive tomorrow.”', 'Your workflow sends arrival information and prompts the team to check the property is ready.', 'You can follow the handoff and get an alert when a task needs attention.'],
      statuses: ['A routine event starts the agreed workflow.', 'Less copying, forwarding and chasing.', 'Your tools and team stay connected.'],
      exception: ['“The cleaner has flagged a maintenance issue.”', 'The workflow alerts the right person and puts the exception in front of you.', 'You or your team decide the fix and confirm the next steps.']
    }
  };

  function render(next, speak = false) {
    const previous = step;
    step = Math.max(0, Math.min(2, next));
    const example = examples[scenario];
    const requiresApproval = approval.checked;
    const text = requiresApproval ? example.exception : example.messages;
    demo.dataset.scenario = scenario;
    demo.dataset.stage = String(step);
    demo.dataset.approval = String(requiresApproval);
    demo.querySelector('[data-demo-title]').textContent = example.title;
    demo.querySelector('[data-message="0"] .sb-message-who').textContent = example.person;
    demo.querySelector('[data-message="1"] .sb-message-who').textContent = scenario === 'operations' ? 'Your workflow' : 'Your AI agent';
    demo.querySelector('[data-next-label]').textContent = requiresApproval ? 'Your decision' : 'Next step';
    scenarioButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.scenario === scenario)));
    stageButtons.forEach((button, i) => {
      button.classList.toggle('is-current', i === step);
      button.classList.toggle('is-complete', i < step);
      button.setAttribute('aria-pressed', String(i === step));
      button.querySelector('strong').textContent = example.steps[i];
      demo.querySelector(`[data-step-detail="${i}"]`).textContent = requiresApproval && i === 2 ? 'You decide before the next step.' : example.details[i];
    });
    messages.forEach((message, i) => {
      message.querySelector('[data-message-text]').textContent = text[i];
      const visible = i <= step;
      message.classList.toggle('is-pending', !visible);
      message.setAttribute('aria-hidden', String(!visible));
      message.classList.remove('is-entering');
      if (i === step && step !== previous && !reduced.matches) {
        void message.offsetWidth;
        message.classList.add('is-entering');
      }
    });
    demo.querySelector('[data-demo-status]').textContent = requiresApproval && step > 0
      ? (step === 1 ? 'The exception comes to you.' : 'You stay in control of the decision.')
      : example.statuses[step];
    stageSurface.setAttribute('data-sc-verify-state', `${scenario}:${step}:${requiresApproval ? 'approval' : 'routine'}:messages-${step + 1}`);
    stageSurface.setAttribute('data-sc-verify-hold', 'true');
    if (speak) announcement.textContent = `${example.steps[step]}. ${text[step]}`;
  }

  function trackChoice() {
    window.strBoosterTrack?.('workflow_example', { scenario, requires_approval: approval.checked, step: step + 1 });
  }
  scenarioButtons.forEach(button => button.addEventListener('click', () => {
    scenario = button.dataset.scenario;
    render(2, true);
    trackChoice();
  }));
  stageButtons.forEach(button => button.addEventListener('click', () => {
    render(Number(button.dataset.stage), true);
    trackChoice();
  }));
  approval.addEventListener('change', () => { render(2, true); trackChoice(); });

  function reportHeroState() {
    if (!heroPinned) {
      heroStage.dataset.scVerifyState = 'connected-static';
      heroStage.dataset.scVerifyHold = 'true';
      return;
    }
    const rect = hero.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > innerHeight) return;
    const p = Math.max(0, Math.min(1, parseFloat(getComputedStyle(hero).getPropertyValue('--sc-p')) || 0));
    const assembled = Math.min(1, p / .86);
    // These values are the same transforms/line reveal painted by the CSS,
    // not a raw scroll counter standing in for visible change.
    heroStage.dataset.scVerifyState = `core-tilt-${(12 * (1 - assembled)).toFixed(1)}:node-spread-${(30 * (1 - assembled)).toFixed(1)}:connection-${assembled.toFixed(2)}`;
    heroStage.dataset.scVerifyHold = String(assembled >= 1);
  }

  function onScroll() {
    if (frame || document.hidden) return;
    frame = requestAnimationFrame(() => { frame = 0; reportHeroState(); });
  }

  function configureMotion() {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    engine?.destroy();
    engine = null;
    heroPinned = desktop.matches && !reduced.matches && Boolean(window.ScrollCraft);
    hero.dataset.scAct = heroPinned ? 'pin' : 'flow';
    hero.classList.toggle('has-hero-motion', heroPinned);
    hero.classList.remove('sc-act--pinned');
    hero.style.removeProperty('height');
    hero.style.removeProperty('--sc-p');
    heroStage.classList.remove('sc-stage');
    workflow.dataset.scAct = 'flow';
    document.querySelectorAll('[data-enter]').forEach(element => {
      if (!reduced.matches && window.ScrollCraft) element.setAttribute('data-sc-in', '');
      else {
        element.removeAttribute('data-sc-in');
        element.style.removeProperty('opacity');
        element.style.removeProperty('transform');
        element.classList.add('sc-in');
      }
    });
    document.querySelectorAll('[data-sc-reveal]').forEach(element => element.style.removeProperty('clip-path'));
    if (window.ScrollCraft && !reduced.matches) {
      try { engine = ScrollCraft.mount(document.querySelector('main')); }
      catch (error) {
        heroPinned = false;
        hero.dataset.scAct = 'flow';
        hero.classList.remove('has-hero-motion', 'sc-act--pinned');
        hero.style.removeProperty('height');
        heroStage.classList.remove('sc-stage');
        document.querySelectorAll('[data-sc-in]').forEach(element => element.classList.add('sc-in'));
        console.warn('Scroll enhancement could not start.', error);
      }
    }
    reportHeroState();
  }

  demo.classList.add('is-interactive');
  render(2);
  configureMotion();
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll, { passive: true });
  document.addEventListener('visibilitychange', () => { if (!document.hidden) onScroll(); });
  reduced.addEventListener('change', configureMotion);
  desktop.addEventListener('change', configureMotion);
  document.fonts?.ready.then(onScroll);
  document.querySelectorAll('.sb-questions details').forEach(item => item.addEventListener('toggle', () => {
    if (!item.open) return;
    document.querySelectorAll('.sb-questions details').forEach(other => { if (other !== item) other.open = false; });
  }));
})();
