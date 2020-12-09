//gulpfile.js
var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var templateCache = require('gulp-angular-templatecache');

//script paths
var jsFiles = ['app/app.js', 'app/modules/**/*.js']
    jsDest = '../static/js';


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
      .pipe(rename('styles.min.css'))
      .pipe(gulp.dest('../static/css/'));
});

gulp.task('js_vendor', function() {
    return gulp.src(['app/lib/angular/angular.js',
                     'app/lib/angular-route/angular-route.js'])
        //.pipe(uglify())
        .pipe(concat('vendor.min.js'))
        //.pipe(rename('vendor.min.js'))
        .pipe(gulp.dest(jsDest))
});

gulp.task('js_app', function() {
    return gulp.src(jsFiles)
        .pipe(concat('scripts.js'))
        .pipe(uglify())
        .pipe(rename('scripts.min.js'))
        .pipe(gulp.dest(jsDest));
});

gulp.task('js', gulp.parallel('js_vendor', 'js_app'));

gulp.task('test', function(done) {

});

gulp.task('default', gulp.parallel('templates', 'css', 'js'));
