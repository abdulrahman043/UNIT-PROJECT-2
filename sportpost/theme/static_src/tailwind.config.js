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
          gridColumn: {
            'span-13': 'span 13 / span 13',
            'span-14': 'span 14 / span 14',
            'span-15': 'span 15 / span 15',
            'span-16': 'span 16 / span 16',
            'span-17': 'span 17 / span 17',
            'span-18': 'span 18 / span 18',
            'span-19': 'span 19 / span 19',
            'span-20': 'span 20 / span 20',
            'span-21': 'span 21 / span 21',
            'span-22': 'span 22 / span 22',
            'span-23': 'span 23 / span 23',
            'span-24': 'span 24 / span 24',
          },
          gridRow: {
            'span-13': 'span 13 / span 13',
            'span-14': 'span 14 / span 14',
            'span-15': 'span 15 / span 15',
            'span-16': 'span 16 / span 16',
            'span-17': 'span 17 / span 17',
            'span-18': 'span 18 / span 18',
            'span-19': 'span 19 / span 19',
            'span-20': 'span 20 / span 20',
            'span-21': 'span 21 / span 21',
            'span-22': 'span 22 / span 22',
            'span-23': 'span 23 / span 23',
            'span-24': 'span 24 / span 24',
          },
          gridColumnStart: {
            '13': '13',
            '14': '14',
            '15': '15',
            '16': '16',
            '17': '17',
            '18': '18',
            '19': '19',
            '20': '20',
            '21': '21',
            '22': '22',
            '23': '23',
            '24': '24',
          },
          gridRowStart: {
            '13': '13',
            '14': '14',
            '15': '15',
            '16': '16',
            '17': '17',
            '18': '18',
            '19': '19',
            '20': '20',
            '21': '21',
            '22': '22',
            '23': '23',
            '24': '24',
          },
          gridColumnEnd: {
            '13': '13',
            '14': '14',
            '15': '15',
            '16': '16',
            '17': '17',
            '18': '18',
            '19': '19',
            '20': '20',
            '21': '21',
            '22': '22',
            '23': '23',
            '24': '24',
          },
          gridRowEnd: {
            '13': '13',
            '14': '14',
            '15': '15',
            '16': '16',
            '17': '17',
            '18': '18',
            '19': '19',
            '20': '20',
            '21': '21',
            '22': '22',
            '23': '23',
            '24': '24',
          },
          gridTemplateColumns: {
            '13': 'repeat(13, minmax(0, 1fr))',
            '14': 'repeat(14, minmax(0, 1fr))',
            '15': 'repeat(15, minmax(0, 1fr))',
            '16': 'repeat(16, minmax(0, 1fr))',
            '17': 'repeat(17, minmax(0, 1fr))',
            '18': 'repeat(18, minmax(0, 1fr))',
            '19': 'repeat(19, minmax(0, 1fr))',
            '20': 'repeat(20, minmax(0, 1fr))',
            '21': 'repeat(21, minmax(0, 1fr))',
            '22': 'repeat(22, minmax(0, 1fr))',
            '23': 'repeat(23, minmax(0, 1fr))',
            '24': 'repeat(24, minmax(0, 1fr))',
          },
          gridTemplateRows: {
            '13': 'repeat(13, minmax(0, 1fr))',
            '14': 'repeat(14, minmax(0, 1fr))',
            '15': 'repeat(15, minmax(0, 1fr))',
            '16': 'repeat(16, minmax(0, 1fr))',
            '17': 'repeat(17, minmax(0, 1fr))',
            '18': 'repeat(18, minmax(0, 1fr))',
            '19': 'repeat(19, minmax(0, 1fr))',
            '20': 'repeat(20, minmax(0, 1fr))',
            '21': 'repeat(21, minmax(0, 1fr))',
            '22': 'repeat(22, minmax(0, 1fr))',
            '23': 'repeat(23, minmax(0, 1fr))',
            '24': 'repeat(24, minmax(0, 1fr))',
          }
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
        require('@tailwindcss/aspect-ratio'),
    ],
}
