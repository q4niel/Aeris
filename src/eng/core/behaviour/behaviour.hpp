#pragma once

namespace ars {
    class Behaviour {
    protected:
        Behaviour();
        virtual ~Behaviour();

        virtual void start();
        virtual void postStart();

        virtual void tick();
        virtual void postTick();

        virtual void end();
    };
}