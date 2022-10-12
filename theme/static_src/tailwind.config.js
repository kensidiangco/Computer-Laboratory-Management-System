/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            fontFamily: {
                display: ['Open Sans', 'sans-serif'],
                body: ['Open Sans', 'sans-serif'],
              },
            extend: {
                fontSize: {
                    14: '14px',
                },
                backgroundColor: {
                    'main-bg': '#FAFBFB',
                    'main-dark-bg': '#20232A',
                    'secondary-dark-bg': '#33373E',
                    'light-gray': '#F7F7F7',
                    'half-transparent': 'rgba(0, 0, 0, 0.5)',
                },
                borderWidth: {
                    1: '1px',
                },
                borderColor: {
                    color: 'rgba(0, 0, 0, 0.1)',
                },
                width: {
                    400: '400px',
                    760: '760px',
                    780: '780px',
                    800: '800px',
                    1000: '1000px',
                    1200: '1200px',
                    1400: '1400px',
                },
                height: {
                    80: '80px',
                },
                minHeight: {
                    590: '590px',
                },
                backgroundImage: {
                    'hero-pattern':
                        "url('https://demos.wrappixel.com/premium-admin-templates/react/flexy-react/main/static/media/welcome-bg-2x-svg.25338f53.svg')",
                },
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
