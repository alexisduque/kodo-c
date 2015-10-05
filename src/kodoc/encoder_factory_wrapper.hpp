// Copyright Steinwurf ApS 2014.
// Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
// See accompanying file LICENSE.rst or
// http://www.steinwurf.com/licensing

#pragma once

#include <cstdint>

#include "factory_wrapper.hpp"
#include "encoder_wrapper.hpp"
#include "kodo_encoder.hpp"

namespace kodo
{
    template<class KodoStack>
    class encoder_factory_wrapper : public factory_wrapper<KodoStack>
    {
    public:

        encoder_factory_wrapper(uint32_t max_symbols,
                                uint32_t max_symbol_size) :
            factory_wrapper<KodoStack>(max_symbols, max_symbol_size)
        { }

        virtual void* build()
        {
            auto encoder = m_factory.build();
            auto wrapper = new encoder_wrapper<KodoStack, kodo_encoder>(
                encoder);

            return wrapper;
        }

    protected:

        using factory_wrapper<KodoStack>::m_factory;
    };
}
