cmake `
    -S . `
    -B build `
    -G Ninja `
    -DCMAKE_BUILD_TYPE=Debug `
    -DPYTHON_EXECUTABLE="${env:python_path}\python.exe"

cmake --build build --config Release --clean-first --target hidapi-py