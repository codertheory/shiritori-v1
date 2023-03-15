declare module "nuxt/schema" {
    // eslint-disable-next-line no-unused-vars
    interface RuntimeConfig {
        public: {
            env: string;
            apiHost: string;
        };
    }
}
// It is always important to ensure you import/export something when augmenting a type
export {};
