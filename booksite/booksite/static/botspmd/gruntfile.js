module.exports = function(grunt) {

    "use strict";

    grunt.initConfig({

        less: {
            production: {
                options: {
                    paths: ["less"]
                },
                files: {
                    "css/material.css": "less/material.less",
                    "css/material-wfont.css": "less/material-wfont.less",
                    "css/ripples.css": "less/ripples.less"
                }
            }
        },

        autoprefixer: {
            options: {
                browsers: ["last 3 versions", "ie 8", "ie 9", "ie 10", "ie 11"]
            },
            dist: {
                files: {
                    "css/material.css": "css/material.css",
                    "css/material-wfont.css": "css/material-wfont.css",
                    "css/ripples.css": "css/ripples.css"
                }
            },
        },

        cssmin: {
            minify: {
                expand: true,
                cwd: "css/",
                src: ["*.css", "!*.min.css"],
                dest: "css/",
                ext: ".min.css"
            }
        },

        copy: {
            css: {
                src: "css/*.min.css",
                dest: "template/material/"
            },
            js: {
                src: "scripts/*.js",
                dest: "template/material/"
            }

        }

    });
    grunt.loadNpmTasks("grunt-contrib-less");
    grunt.loadNpmTasks("grunt-autoprefixer");
    grunt.loadNpmTasks("grunt-contrib-cssmin");
    grunt.loadNpmTasks("grunt-contrib-copy");
    grunt.registerTask("default", ["less", "autoprefixer", "cssmin", "copy"]);
};
