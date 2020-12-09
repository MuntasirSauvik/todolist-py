//gulpfile.js
var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');

//script paths
var jsFiles = ['app/modules/**/*.js', 'app/*.js']
    jsDest = 'static/js';

gulp.task('templates', function(done) {
  done();
});

gulp.task('css', function(done) {
  done();
});

gulp.task('scripts', function() {
    return gulp.src(jsFiles)
        .pipe(concat('scripts.js'))
        .pipe(gulp.dest(jsDest))
        .pipe(rename('scripts.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest(jsDest));
});

gulp.task('default', gulp.parallel('templates', 'css', 'scripts'));
