twelve_tet = 440*2^(1/12).^linspace(-54,53,108);
%stem(twelve_tet)
pitches = [396 397 880 1234];
i = 1;
for p = pitches
    [nearest, cents, partial] = near_pitch(p);

    fprintf("Pitch: %4.3f\n", p)
    fprintf("Nearest: %4.3f\n", nearest)
    fprintf("Cents: %4.3f\n", cents)
    fprintf("Partial: %4.3f  %4.3f  %4.3f\n", partial);
    figure(i)
    hold on
    plot(twelve_tet)
    xlim([12*log2(nearest/440)+54.5 12*log2(partial(3)/440)+55.5])
    scatter(12*log2([nearest partial]./440)+55, [nearest partial])

    i = i + 1;
end


function [nearest,cents,partial] = near_pitch(f0)
    twelve_tet = 440*2^(1/12).^linspace(-54,53,108);

    idx = find(abs(1200*log2(f0./twelve_tet))<=50, 1);
    nearest = twelve_tet(idx);

    cents = 1200*log2(f0/twelve_tet(idx));

    partial = f0*2^(1/1200).^[-0.25*cents -0.5*cents -0.75*cents];
end
