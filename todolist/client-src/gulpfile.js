//gulpfile.js
var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var templateCache = require('gulp-angular-templatecache');
var cleanCSS = require('gulp-clean-css');
var sourcemaps = require('gulp-sourcemaps');
var browserify = require('browserify');
var watchify = require('watchify');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var log = require('gulplog');
var assign = require('lodash.assign');

//script paths
var jsFiles = ['app/app.js']
    jsDest = '../static/js';

// add custom browserify options here
var customOpts = {
  entries: jsFiles,
  debug: true
};

var opts = assign({}, watchify.args, customOpts);
var b = watchify(browserify(opts));

// add transformations here
// i.e. b.transform(coffeeify);


gulp.task('js_app', js_app); // so you can run `gulp js` to build the file
b.on('update', js_app); // on any dep update, runs the bundler
b.on('log', log.info); // output build logs to terminal

function js_app() {
  return b.bundle()
    // log errors if they happen
    .on('error', log.error.bind(log, 'Browserify Error'))
    .pipe(source('bundle.js'))
    // optional, remove if you don't need to buffer file contents
    .pipe(buffer())
    // optional, remove if you dont want sourcemaps
    .pipe(sourcemaps.init({loadMaps: true})) // loads map from browserify file
       // Add transformation tasks to the pipeline here.
    .pipe(sourcemaps.write('./')) // writes .map file
    .pipe(gulp.dest('./dist'));
}

/*gulp.task('js_app', function() {
    return gulp.src(jsFiles)
        .on('error', log.error.bind(log, 'Browserify Error'))
        .pipe(sourcemaps.init())
        .pipe(concat('scripts.js'))
        .pipe(uglify())
        .pipe(rename('scripts.min.js'))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(jsDest));
});*/

gulp.task('templates_app', function() {

  return gulp.src('app/app.html')
      .pipe(rename('app.mako'))
      .pipe(gulp.dest('../templates/'));

});

gulp.task('templates_modules', function() {

  return gulp.src('app/modules/**/*.html')
    .pipe(templateCache({root: 'modules', standalone: true}))
    .pipe(rename('templates.min.js'))
    .pipe(gulp.dest(jsDest));

});

gulp.task('templates', gulp.parallel('templates_app', 'templates_modules'));

gulp.task('css', function() {
  return gulp.src('app/app.css')
      .pipe(sourcemaps.init())
      .pipe(cleanCSS())
      .pipe(rename('styles.min.css'))
      .pipe(sourcemaps.write())
      .pipe(gulp.dest('../static/css/'));
});

gulp.task('js_vendor', function() {
    return gulp.src(['app/lib/angular/angular.js',
                     'app/lib/angular-route/angular-route.js'])
        .pipe(sourcemaps.init())
        //.pipe(uglify())
        .pipe(concat('vendor.min.js'))
        //.pipe(rename('vendor.min.js'))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(jsDest))
});

gulp.task('js', gulp.parallel('js_vendor', 'js_app'));

gulp.task('test', function(done) {

});

gulp.task('default', gulp.parallel('templates', 'css', 'js'));
