/* Page-specific behaviour. Scrollcraft is vendored without modification. */
(() => {
  'use strict';
  document.documentElement.classList.add('has-js');

  const demo = document.querySelector('[data-demo]');
  if (!demo) return;
  const workflow = document.querySelector('#how-it-works');
  const stageSurface = workflow.querySelector('[data-sc-stage]');
  const stageButtons = [...demo.querySelectorAll('[data-stage]')];
  const scenarioButtons = [...demo.querySelectorAll('[data-scenario]')];
  const messages = [...demo.querySelectorAll('[data-message]')];
  const approval = document.querySelector('#approval-toggle');
  const announcement = demo.querySelector('[data-demo-announcement]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const desktop = matchMedia('(min-width: 1024px) and (min-height: 760px)');
  let scenario = 'booking';
  let step = 0;
  let engine = null;
  let pinned = false;
  let frame = 0;
  let manual = false;
  let manualProgress = 0;

  const examples = {
    booking: {
      title: 'From interest to booking',
      person: 'Guest',
      details: ['A guest asks about your property.', 'Your approved information does the work.', 'A clear route to your booking engine.'],
      messages: ['“Would your place suit a family weekend?”', 'Shares the family-friendly details you have approved, then helps with the next question.', 'The guest checks dates and completes their reservation through your booking engine.'],
      statuses: ['A potential guest has a question.', 'Helpful answers, based on your property.', 'Your booking engine handles dates and payment.'],
      exception: ['“Could we check in early on Friday?”', 'Explains that early check-in needs confirmation. It does not promise a time without approval.', 'You or your team receive the request and decide. The guest gets your confirmed answer.']
    },
    concierge: {
      title: 'A useful answer, without the repeat admin',
      person: 'Guest',
      details: ['A guest needs practical information.', 'Your property guide supplies the answer.', 'The guest knows what to do next.'],
      messages: ['“Where can we park when we arrive?”', 'Shares the parking and arrival instructions from the property information you have approved.', 'The guest has the instructions. Anything outside the agreed guidance comes to you or your team.'],
      statuses: ['An everyday guest question.', 'Your information, ready when guests need it.', 'Routine questions handled. Exceptions stay visible.'],
      exception: ['“Can we bring an extra guest tonight?”', 'Explains that a change to the reservation needs the host’s approval. It does not change the booking.', 'You review the request against your rules and capacity before confirming the answer.']
    },
    owner: {
      title: 'From owner interest to a sales conversation',
      person: 'Property owner',
      details: ['An owner asks about your service.', 'The system gathers relevant details.', 'A qualified conversation reaches your team.'],
      messages: ['“Could you help manage my holiday home?”', 'Asks about the property, location and owner’s goals using the questions you have agreed.', 'A suitable enquiry is invited to a discovery call. Your team sees the context for the conversation.'],
      statuses: ['A new opportunity for your management business.', 'Relevant questions, consistent follow-up.', 'Your team takes the sales conversation forward.'],
      exception: ['“Can you guarantee what my property will earn?”', 'Explains that income depends on the property and market. It makes no revenue promise.', 'The owner is referred to your team for a property review and a properly scoped discussion.']
    }
  };

  function progress() {
    return Math.max(0, Math.min(1, parseFloat(getComputedStyle(workflow).getPropertyValue('--sc-p')) || 0));
  }

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
    demo.querySelector('[data-next-label]').textContent = requiresApproval ? 'Your decision' : 'Next step';
    scenarioButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.scenario === scenario)));
    stageButtons.forEach((button, i) => {
      button.classList.toggle('is-current', i === step);
      button.classList.toggle('is-complete', i < step);
      button.setAttribute('aria-pressed', String(i === step));
      demo.querySelector(`[data-step-detail="${i}"]`).textContent = requiresApproval && i === 2 ? 'You decide before anything is promised.' : example.details[i];
    });
    messages.forEach((message, i) => {
      message.querySelector('[data-message-text]').textContent = text[i];
      const visible = i <= step;
      message.classList.toggle('is-pending', !visible);
      message.setAttribute('aria-hidden', String(!visible));
      message.classList.remove('is-entering');
      if (i === step && step !== previous && !reduced.matches) {
        // Re-trigger only a newly revealed message, never every scroll frame.
        void message.offsetWidth;
        message.classList.add('is-entering');
      }
    });
    const status = requiresApproval && step > 0
      ? (step === 1 ? 'No promise made before your approval.' : 'You stay in control of the decision.')
      : example.statuses[step];
    demo.querySelector('[data-demo-status]').textContent = status;
    stageSurface.setAttribute('data-sc-verify-state', `${scenario}:${step}:${requiresApproval ? 'approval' : 'routine'}:messages-${step + 1}`);
    if (speak) announcement.textContent = `${stageButtons[step].querySelector('strong').textContent}. ${text[step]}`;
  }

  function userChoice() {
    manual = true;
    manualProgress = progress();
    window.strBoosterTrack?.('workflow_example', { scenario, requires_approval: approval.checked, step: step + 1 });
  }

  scenarioButtons.forEach(button => button.addEventListener('click', () => {
    scenario = button.dataset.scenario;
    render(2, true);
    userChoice();
  }));
  stageButtons.forEach(button => button.addEventListener('click', () => {
    render(Number(button.dataset.stage), true);
    userChoice();
  }));
  approval.addEventListener('change', () => {
    render(2, true);
    userChoice();
  });

  function onScroll() {
    if (!pinned || frame || document.hidden) return;
    frame = requestAnimationFrame(() => {
      frame = 0;
      const p = progress();
      if (manual && Math.abs(p - manualProgress) < .13) return;
      manual = false;
      const next = p < .27 ? 0 : p < .61 ? 1 : 2;
      if (next !== step) render(next);
      stageSurface.setAttribute('data-sc-verify-hold', String(p >= .92));
    });
  }

  function configureMotion() {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    engine?.destroy();
    engine = null;
    pinned = desktop.matches && !reduced.matches && Boolean(window.ScrollCraft);
    workflow.dataset.scAct = pinned ? 'pin' : 'flow';
    workflow.classList.remove('sc-act--pinned');
    workflow.style.removeProperty('height');
    workflow.style.removeProperty('--sc-p');
    stageSurface.classList.remove('sc-stage');
    stageSurface.removeAttribute('data-sc-verify-hold');
    document.querySelectorAll('[data-depth]').forEach(layer => {
      layer.style.removeProperty('transform');
      if (desktop.matches && !reduced.matches) layer.setAttribute('data-sc-parallax', layer.dataset.depth);
      else layer.removeAttribute('data-sc-parallax');
    });
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
        // All content and call links remain usable if enhancement is unavailable.
        pinned = false;
        workflow.dataset.scAct = 'flow';
        workflow.style.removeProperty('height');
        workflow.classList.remove('sc-act--pinned');
        stageSurface.classList.remove('sc-stage');
        document.querySelectorAll('[data-sc-in]').forEach(element => element.classList.add('sc-in'));
        console.warn('Scroll enhancement could not start.', error);
      }
    } else {
      document.querySelectorAll('[data-sc-count]').forEach(element => {
        element.textContent = element.dataset.scCount.trim().split(/\s+/)[1];
      });
    }
    manual = false;
    render(pinned ? 0 : 2);
    onScroll();
  }

  demo.classList.add('is-interactive');
  configureMotion();
  addEventListener('scroll', onScroll, { passive: true });
  document.addEventListener('visibilitychange', () => { if (!document.hidden) onScroll(); });
  reduced.addEventListener('change', configureMotion);
  desktop.addEventListener('change', configureMotion);
  document.querySelectorAll('.sb-questions details').forEach(item => item.addEventListener('toggle', () => {
    if (!item.open) return;
    document.querySelectorAll('.sb-questions details').forEach(other => { if (other !== item) other.open = false; });
  }));
})();
