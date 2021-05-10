var gulp = require('gulp'),
	autoprefixer = require('gulp-autoprefixer'),
	sass = require('gulp-sass'),
    browserSync = require('browser-sync').create();


 
gulp.task('sass', function() {
  return gulp.src('scss/style.scss')
    .pipe(sass({outputStyle: 'compact'}))
    .pipe(autoprefixer( {browsers:['> 1%', 'last 2 versions', 'ie >= 9', 'Opera >= 12', 'Firefox >= 3.6', 'Chrome >= 19']}))
    .pipe(gulp.dest('css'))
});

gulp.task('html', function() {
	return gulp.src('*.html')
});


gulp.task('browser-sync', function() {
    browserSync.init(["css/*.css", "script/*.js", "*.html"],{
        server: {
            baseDir: "./"
        }
    });
});

gulp.task('watch', function() {
	gulp.watch('scss/*.scss', ['sass'])
	gulp.watch('*.html', ['html'])
});

gulp.task('default', ['sass', 'watch', 'html', 'browser-sync']);