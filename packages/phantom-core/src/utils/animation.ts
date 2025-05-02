// packages/phantom-core/src/utils/animation.ts
// TODO: Do we need to remove this?

const animation = {
  fadeIn: (duration = '0.3s') => ({
    animation: `fadeIn ${duration} ease-in-out`,
  }),
};

export default animation;