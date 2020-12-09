'use strict';
var gulp = require('gulp');
var gulp_if = require('gulp-if');
var sass = require('gulp-sass');
var debug = require('gulp-debug');
var rename = require('gulp-rename');
var concat = require('gulp-concat');
var sourcemaps = require('gulp-sourcemaps');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var browserify = require('browserify');
var babel = require('babelify');
var clean_css = require('gulp-clean-css');
var uglify = require('gulp-uglify');
var watchify = require('watchify');
var templateCache = require('gulp-angular-templatecache');
var filesExist = require('files-exist');
var log = require('fancy-log');

var APP_CSS_GLOBS = ['styles/app/**/*.scss'];
var LIB_TEMPLATE_GLOBS = ['lib/templates/**/*.html'];
var MODULE_TEMPLATE_GLOBS = ['modules/*/templates/**/*.html'];
var APP_TEMPLATE_GLOBS = [];
    APP_TEMPLATE_GLOBS.push.apply(APP_TEMPLATE_GLOBS, LIB_TEMPLATE_GLOBS);
    APP_TEMPLATE_GLOBS.push.apply(APP_TEMPLATE_GLOBS, MODULE_TEMPLATE_GLOBS);

var DEVELOPMENT_MODE = true;

gulp.task('vendor_css', function() {
    return gulp.src(filesExist([
        'node_modules/bootstrap/dist/css/bootstrap.css',
        'node_modules/font-awesome/css/font-awesome.css',
        'node_modules/ui-select/dist/select.css',
        'node_modules/angular-toastr/dist/angular-toastr.css',
        'node_modules/angular-moment-picker/dist/angular-moment-picker.css',
        'node_modules/fullcalendar/dist/fullcalendar.css',
        'node_modules/angular-bootstrap-colorpicker/css/colorpicker.css',
        'node_modules/angular-block-ui/dist/angular-block-ui.css',,
        'node_modules/ng-image-gallery/dist/ng-image-gallery.css',
        'node_modules/textangular/dist/textAngular.css',
        'styles/minovate/minovate.css'
    ]))
    .pipe(gulp_if(DEVELOPMENT_MODE, sourcemaps.init({ loadMaps: true })))
    .pipe(gulp_if(MINIFY_VENDOR_CSS, clean_css()))
    .pipe(gulp_if(DEVELOPMENT_MODE, sourcemaps.write('./')))
    .pipe(concat('vendor.css'))
    .pipe(gulp.dest('../static/css'))
});

gulp.task('vendor_js', function() {
    return gulp.src(filesExist([
        'node_modules/lodash/lodash.js',
        'node_modules/jquery/dist/jquery.js',
        //'node_modules/bootstrap/dist/js/bootstrap.js',
        'node_modules/moment/moment.js',
        'node_modules/toastr/toastr.js',
        'node_modules/angular/angular.js',
        'node_modules/url-template/lib/url-template.js',
        'node_modules/angular-animate/angular-animate.js',
        //'node_modules/angular-sanitize/angular-sanitize.js',
        'node_modules/@uirouter/angularjs/release/angular-ui-router.js',
        'node_modules/ui-select/dist/select.js',
        'node_modules/angular-ui-bootstrap/dist/ui-bootstrap.js',
        'node_modules/angular-ui-bootstrap/dist/ui-bootstrap-tpls.js',
        'node_modules/angular-toastr/dist/angular-toastr.js',
        'node_modules/angular-toastr/dist/angular-toastr.tpls.js',
        'node_modules/angular-fontawesome/dist/angular-fontawesome.js',
        'node_modules/jquery-slimscroll/jquery.slimscroll.js',
        'node_modules/angular-local-storage/dist/angular-local-storage.js',
        'node_modules/angular-filter/dist/angular-filter.js',
        'node_modules/angular-moment-picker/dist/angular-moment-picker.js',
        'node_modules/fullcalendar/dist/fullcalendar.js',
        'node_modules/angular-ui-calendar/src/calendar.js',
        'node_modules/chart.js/dist/Chart.js',
        'node_modules/chartjs-plugin-datalabels/dist/chartjs-plugin-datalabels.js',
        'node_modules/angular-chart.js/dist/angular-chart.js',
        'node_modules/angular-bootstrap-colorpicker/js/bootstrap-colorpicker-module.js',
        'node_modules/angular-file-upload/dist/angular-file-upload.js',
        'node_modules/angular-block-ui/dist/angular-block-ui.js',
        'node_modules/angular-tablesort/js/angular-tablesort.js',
        'node_modules/ng-image-gallery/dist/ng-image-gallery.js',
        'node_modules/textangular/dist/textAngular-sanitize.min.js',
        'node_modules/textangular/dist/textAngular-rangy.min.js',
        'node_modules/textangular/dist/textAngularSetup.js',
        'node_modules/textangular/dist/textAngular.js'
    ]))
    .pipe(gulp_if(MINIFY_VENDOR_JS, uglify()))
    .pipe(concat('vendor.js'))
    .pipe(gulp.dest('../static/js'))
});

gulp.task('vendor', gulp.series('vendor_js', 'vendor_css'));

gulp.task('app_html', function() {
    return gulp.src('app.html')
        .pipe(rename('app.mak'))
        .pipe(gulp.dest('../templates/'))
});

gulp.task('app_css', gulp.series('app_sass', function() {
    return gulp.src(['styles/app/**/*.css'])
        .pipe(gulp_if(MINIFY_APP_CSS, clean_css()))
        .pipe(concat('app.css'))
        .pipe(gulp.dest('../static/css'));
}));

function build_js(do_watch) {
	var bundler = browserify('./app.js', {debug: true})
        .transform(babel, {presets: ['@babel/preset-env']});

	function do_bundle() {
        return bundler.bundle()
          .on('error', function(err) { console.error(err.message); this.emit('end'); })
          .pipe(source('app.js'))
          .pipe(buffer())
          .pipe(gulp_if(DEVELOPMENT_MODE, sourcemaps.init({ loadMaps: true })))
          .pipe(gulp_if(MINIFY_APP_JS, uglify({mangle: false})))
          .pipe(gulp_if(DEVELOPMENT_MODE, sourcemaps.write('./')))
          .pipe(gulp.dest('../static/js'));
    }

    if(do_watch) {
        var watcher = watchify(bundler);
        do_bundle();
        watcher.on('update', function() {
            log('Bundling...');
            do_bundle();
        });
        return watcher;
    } else {
        return do_bundle();
    }
}

gulp.task('app_images', function() {
    return gulp.src(['images/app/**/*'])
        .pipe(gulp.dest('../static/images'))
});

gulp.task('app_js', function() {
    return build_js();
});

gulp.task('app_js_watch', function() {
    return build_js(true);
});

gulp.task('initial_sass', function() {
    return gulp.src(['styles/initial/initial.scss'])
        .pipe(sass({
            //includePaths: require('node-bourbon').includePaths
        }))
        .pipe(rename('initial.css'))
        .pipe(gulp.dest('styles/initial'))
});

gulp.task('initial_css', gulp.series('initial_sass', function() {
    return gulp.src(['styles/initial/initial.css'])
    .pipe(gulp_if(MINIFY_VENDOR_CSS, clean_css()))
    .pipe(concat('initial.css'))
    .pipe(gulp.dest('../static/css'))
}));

gulp.task('initial', gulp.series('initial_css'));

gulp.task('app', gulp.series('app_html', 'app_images', 'app_js', 'app_css', 'app_templates', 'initial'));

gulp.task('watch', gulp.series('app', function() {
    gulp.watch(['app.html'], gulp.series('app_html'));
    gulp.watch(APP_CSS_GLOBS, gulp.series('app_css'));
    gulp.watch(APP_TEMPLATE_GLOBS, gulp.series('app_templates'));
    build_js(true);
}));

gulp.task('full', gulp.series('vendor', 'app'));

gulp.task('default', gulp.series('full'));
