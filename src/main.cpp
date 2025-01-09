int entry(int argc, char **argv) {
    return 0;
}

#ifdef PLATFORM_LINUX
int main(int argc, char **argv) {
    return entry(argc, argv);
}
#endif